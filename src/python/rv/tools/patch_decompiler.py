import argparse
import logging
import math
import os
import random
import re
import sys

from rv.api import NOTECMD, Note, Pattern, PatternClone, Project, read_sunvox_file

log = logging.getLogger(__name__)

IGNORE = ["Compressor"]


def init_logger():
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    root.addHandler(handler)


def class_name(mod):
    return [tok for tok in re.split("\\W", str(mod.__class__)) if tok not in [""]][-1]


class ModuleChain(list):
    @staticmethod
    def expand(proj):
        mods = {mod.index: mod for mod in proj.modules if hasattr(mod, "index")}
        # [TODO] proj.module_connections was removed in Radiant Voices 1.0.
        # This code must be rewritten for compatibility.
        connections = dict(proj.module_connections)
        chains = []

        def expand(i, state=[]):
            if i in state:
                log.warning(f"ignoring loop {i} -> {state}")
                return
            state.append(i)
            if not connections[i]:
                chains.append(state)
            for j in connections[i]:
                if j in connections:
                    expand(j, list(state))

        expand(0)
        return [
            ModuleChain(
                [mods[i] for i in reversed(chain) if class_name(mods[i]) not in IGNORE]
            )
            for chain in chains
        ]

    def __init__(self, mods):
        list.__init__(self, mods)

    @property
    def modules(self):
        return [mod.index for mod in self]

    @property
    def mapping(self):
        return {mod.index: i for i, mod in enumerate(reversed(self))}

    def detach(self):
        def detach(mod):
            try:
                return mod.clone()
            except Exception as error:
                log.error(f"problem detaching {mod}: {error!s}")
                newmod = mod.__class__()
                for key, value in mod.controller_values.items():
                    setattr(newmod, key, value)
                return newmod

        return [detach(mod) for mod in self]

    def __str__(self):
        return "~".join([str(mod.index) for mod in self])


class Notes(list):
    def __init__(self, notes=[]):
        list.__init__(self, notes)

    def normalise(self, mod):
        for note in self:
            if note.module:
                note.module = mod
        return self

    def __str__(self):
        return "/".join([str(note) for note in self])


class Track(list):
    @staticmethod
    def split(pat):
        tracks, last = {}, None
        for j in range(pat.tracks):
            for i in range(pat.lines):
                note = pat.data[i][j].clone()
                if note.module:
                    note.module -= 1  # NB
                    tracks.setdefault(note.module, Track(pat.lines))
                    track = tracks[note.module]
                    if not track[i]:
                        track[i] = Notes()
                    track[i].append(note)
                    last = note.module
                elif note.note == NOTECMD.NOTE_OFF.value and last is not None:
                    track = tracks[last]
                    track[i].append(note)
                    last = None
        return tracks

    def __init__(self, n):
        list.__init__(self, [Notes() for i in range(n)])

    @property
    def polyphony(self):
        return max(len(notes) for notes in self)

    @property
    def audible(self):
        for notes in self:
            for note in notes:
                if note.note:
                    return True
        return False

    def normalise(self, mod):
        for notes in self:
            notes.normalise(mod)
        return self

    def __str__(self):
        return ",".join(
            [f"{i}:{notes!s}" for i, notes in enumerate(self) if len(notes) != 0]
        )


class Tracks(dict):
    def __init__(self, values={}):
        dict.__init__(self, values)

    @property
    def lines(self):
        return sorted([len(self[mod]) for mod in self if mod in self])[0]

    def subset(self, mods):
        cache = Tracks()
        for mod in mods:
            if mod in self:
                cache[mod] = self[mod]
        return cache

    def normalise(self, mapping):
        for mod in self:
            self[mod].normalise(mapping[mod])
        return self

    @property
    def audible(self):
        return any(track.audible for track in self.values())

    def flatten(self):
        mods = sorted(list(self.keys()))
        index = [(mod, i) for mod in mods for i in range(self[mod].polyphony)]
        pat = Pattern(lines=self.lines, tracks=len(index))

        def notefn(track, i, j):
            mod, k = index[j]
            notes = self[mod][i]
            if k < len(notes):
                note = notes[k].clone()
                if note.module:
                    note.module += 1  # NB
                return note
            else:
                return Note()

        pat.set_via_fn(notefn)
        return pat

    def __str__(self):
        return "|".join([f"{mod}:{self[mod]!s}" for mod in self])


def parse_timeline(proj):
    trackmap, timeline = {}, {}
    for i, pat in enumerate(proj.patterns):
        if isinstance(pat, PatternClone) and pat.source not in trackmap:
            continue
        if not isinstance(pat, PatternClone):
            trackmap[i] = tracks = Track.split(pat)
        else:
            tracks = trackmap[pat.source]
        if len(tracks) == 0:
            continue
        timeline.setdefault(pat.x, Tracks())
        timeline[pat.x].update(tracks)
    return timeline


def decompile(proj):
    chains = ModuleChain.expand(proj)
    timeline = parse_timeline(proj)

    def patch_name(chain, n=3):
        return "-".join(
            [mod.name[:n] for mod in chain if not mod.name.lower().startswith("out")]
        )

    cache, patches = {}, []
    for x in sorted(timeline.keys()):
        tracks = timeline[x]
        for chain in chains:
            name, key = patch_name(chain), str(chain)
            key = str(chain)
            cache.setdefault(key, [])
            group = tracks.subset(chain.modules)
            if len(group) == 0:
                continue
            if key in cache and str(group) in cache[key]:
                continue
            if not group.audible:
                log.warning(f"{name}/{x} is inaudible")
                continue
            pat = group.normalise(chain.mapping).flatten()
            patch = {"name": name, "x": x, "modules": chain.detach(), "pattern": pat}
            patches.append(patch)
            cache[key].append(str(group))
    return patches


def module_layout(n, seed=13, offset=(512, 512), mult=(256, 256), tries=50):
    random.seed(seed)

    def is_neighbour(p, q):
        return (
            (
                (p[0] == q[0] and abs(p[1] - q[1]) == 1)
                or (p[1] == q[1] and abs(p[0] - q[0]) == 1)
            )
        ) and (abs(p[0] - q[0]) != 1 or abs(p[1] - q[1]) != 1)

    def normalise(r):
        return [(i - r[0][0], j - r[0][1]) for i, j in r]

    def sample(n, matcher=is_neighbour, padding=2):
        sz = padding + int(math.ceil(math.sqrt(n)))
        pairs = [(i, j) for i in range(sz) for j in range(sz)]
        q0 = q = tuple([random.choice(range(sz)), random.choice(range(sz))])
        pairs.remove(q)
        r = [q0]
        for _ in range(n - 1):
            adjacent = [p for p in pairs if matcher(p, q)]
            if adjacent == []:
                raise RuntimeError("No adjacent pairs")
            q = random.choice(adjacent)
            pairs.remove(q)
            r.append(q)
        return normalise(r)

    def div_zero(fn):
        def wrapped(r):
            if len(r) == 1:
                return 1
            return fn(r)

        return wrapped

    @div_zero
    def compactness(r):
        head, tail = r[0], r[1:]

        def err(s):
            return sum((s[i] - head[i]) ** 2 for i in range(2))

        return (sum([err(s) for s in tail]) / (len(r) - 1)) ** 0.5

    def best(n, tries):
        best, besterr = None, 1e10
        for _ in range(tries):
            try:
                L = sample(n + 1)
            except RuntimeError:
                continue
            err = compactness(L)
            if err < besterr:
                best, besterr = L, err
        return best[1:]

    def expand(r):
        oi, oj = offset
        mi, mj = mult
        return [(oi + mi * i, oj + mj * j) for i, j in r]

    return expand(best(n, tries))


def dump(props, patch, output_dir, dirname):
    patch_dir = f"{output_dir}/{dirname}/{patch['name']}"
    os.makedirs(patch_dir, exist_ok=True)
    proj = Project()
    proj.initial_bpm = props["bpm"]
    proj.initial_tpl = props["tpl"]
    layout = module_layout(len(patch["modules"]))
    for i, mod in enumerate(reversed(patch["modules"][:-1])):
        mod.x, mod.y = layout[i]
        proj.attach_module(mod)
    for i in range(len(proj.modules) - 1):
        proj.connect(proj.modules[i + 1], proj.modules[i])
    proj.patterns.append(patch["pattern"])
    destfilename = f"{patch_dir}/{patch['x']}.sunvox"
    with open(destfilename, "wb") as f:
        proj.write_to(f)


parser = argparse.ArgumentParser(description="SunVox patch decompiler")
parser.add_argument(
    "--output-dir",
    metavar="PATH",
    type=str,
    default="patch-decompiler-output",
    help="Base directory to write patches to",
)
parser.add_argument(
    "filename", metavar="FILE", type=str, nargs=1, help="SunVox project to decompile"
)


def main():
    init_logger()
    args = parser.parse_args()
    filename = args.filename[0]
    output_dir = args.output_dir
    if not os.path.exists(filename):
        raise RuntimeError("File does not exist")
    if not filename.endswith(".sunvox"):
        raise RuntimeError("File must be a .sunvox file")
    dirname = filename.split("/")[-1].split(".")[0]
    os.makedirs(f"{output_dir}/{dirname}", exist_ok=True)

    proj = read_sunvox_file(filename)
    props = {"bpm": proj.initial_bpm, "tpl": proj.initial_tpl}
    patches = decompile(proj)
    npatches = len(list({patch["name"] for patch in patches}))
    nversions = len(patches)
    log.info(
        f"dumping {npatches} patches [{nversions} versions] to {output_dir}/{dirname}"
    )
    for patch in patches:
        dump(props, patch, output_dir, dirname)


if __name__ == "__main__":
    main()
