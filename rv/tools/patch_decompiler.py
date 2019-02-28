from rv.note import Note, NOTECMD

"""
- some useful Note extensions
- `note`, `vel`, `ctl`, `val` all indicate a Note has some kind of "musical value"; `mod` does not as is just a binding attribute
"""

def note_empty(self):
    return not (self.note or
                self.vel or
                # self.mod or
                self.ctl or
                self.val)

Note.is_empty=note_empty

def note_str(self):
    tokens=[]
    for attr in ["note",
                 "vel",
                 # "mod",
                 "ctl",
                 "val"]:
        if hasattr(self, attr):
            tokens.append("%s%i" % (attr[0],
                                    getattr(self, attr)))
    return "".join(tokens)

Note.__str__=note_str

"""
- ModuleChain is a simple uni-directional list of modules
"""

class ModuleChain(list):

    """
    - expand/1 walks `proj.module_connections` to infer straight- line chains of modules, starting from Output/0
    - returns a ModuleChain with Output/0 at the *end*
    """
    
    @classmethod
    def expand(self, proj):
        mods={mod.index:mod
              for mod in proj.modules}
        connections=dict(proj.module_connections)
        chains=[]
        def expand(i, state=[]):
            state.append(i)
            if connections[i]==[]:
                chains.append(state)
            for j in connections[i]:
                if j in connections:
                    expand(j, list(state))
        expand(0)
        return [ModuleChain([mods[i]
                             for i in reversed(chain)])
                for chain in chains]
    
    def __init__(self, mods):
        list.__init__(self, mods)

    @property
    def modules(self):
        return [mod.index
                for mod in self]

    """
    - mapping/0 returns a "normalised" list of module indexes (starting at zero)
    - [if you create a new project and add new modules to it, module indexation starts at zero; and each new module's index is atomically incremented]
    - [so if you want to import notes from an existing project into a new project, you will need to re-map all the module references contained in the pattern]
    - remember
      - modules are added from Output [0] 
      - chain is "backwards" in that Output is at the end
      - hence need to reverse iterate
    """
    
    @property
    def mapping(self):
        return {mod.index:i
                for i, mod in enumerate(reversed(self))}

    """
    - "detaches" a ModuleChain from an existing project by cloning a module and setting all controller values
    """
    
    def detach(self):
        def clone(mod):
            newmod=mod.__class__()
            for key, value in mod.controller_values.items():
                setattr(newmod, key, value)
            return newmod
        return [clone(mod)
                for mod in self]
    
    def __str__(self):
        return "~".join([str(mod.index)
                         for mod in self])

"""
- a Chord is a list of notes which should be played by the same module at the same time
"""
    
class Chord(list):

    def __init__(self, notes=[]):
        list.__init__(self, notes)

    """
    - normalise/1 remaps all module references with a Chord
    """
        
    def normalise(self, mod):
        for note in self:
            if note.module:
                note.module=mod
        return self

    def __str__(self):
        return "/".join([str(note)
                         for note in self])

"""
- a Track is somewhat analogous to a Sunvox track, ie is a list of Notes; however
- 1) intention is that a Track contains *all* notes for a *single* module only (unlike Sunvox tracks which have no such restriction)
- 2) because you may want a module to play a number of notes at a single point in time, a Track contains Chords rather than Notes
"""
    
class Track(list):    

    """
    - split/1 creates a map of Track objects from a Pattern, with keys set to module index
    - RV "feature" in which modules are indexed at 0 but note.module appears to be indexed at 1
    - need to remove this "feature" as you use note.module for looking up chains via module.index
    - NOTE_OFF is slighly tricky as doesn't contain a module reference; module is last "played" note; hence need to keep track of `last`
    """
    
    @classmethod
    def split(self, pat):
        tracks, last = {}, None
        for j in range(pat.tracks):
            for i in range(pat.lines):
                note=pat.data[i][j]
                if note.module:
                    note.module-=1 # NB
                    tracks.setdefault(note.module,
                                      Track(pat.lines))
                    track=tracks[note.module]
                    if not track[i]:
                        track[i]=Chord()
                    track[i].append(note)
                    last=note.module
                elif (note.note==NOTECMD.NOTE_OFF.value and
                      last!=None):
                    track=tracks[last]
                    track[i].append(note)
                    last=None
        return tracks        

    def __init__(self, n):
        list.__init__(self, [Chord()
                             for i in range(n)])

    """
    - polyphony is max chord length within a Track
    """
        
    @property
    def polyphony(self):
        return max([len(chord)
                    for chord in self])

    """
    - normalise/1 remaps all module references with a Chord
    - remember all Notes within a specific Track should have the same module reference
    """
    
    def normalise(self, mod):
        for chord in self:
            chord.normalise(mod)
        return self

    def __str__(self):
        return ",".join(["%i:%s" % (i, str(chord))
                         for i, chord in enumerate(self)
                         if not len(chord)==0])

"""
- Tracks is a map of {mod:Track} objects
- remember that all Notes for a given module in a given time period should be contained in a single Track
"""
    
class Tracks(dict):

    def __init__(self, values={}):
        dict.__init__(self, values)

    @property
    def lines(self):
        return sorted([len(self[mod])
                       for mod in self
                       if mod in self])[0]

    """
    - group/0 takes a list of module indexes (eg from a ModuleChain), returns the tracks associated with that list
    - is effectively a subset() function
    """
    
    def group(self, mods):
        cache=Tracks()
        for mod in mods:
            if mod in self:
                cache[mod]=self[mod]
        return cache

    """
    - normalise re-maps all Track/Chord/Note module references, typically consistent with the normalised mapping returned by a ModuleChain
    """
    
    def normalise(self, mapping):
        for mod in self:
            self[mod].normalise(mapping[mod])
        return self

    """
    - flatten/0 is an important function in that it "paints" the Track data contained within Tracks onto a single Pattern which is then used as part of the output Project
    - RV "feature" in which modules are indexed at 0 but note.module appears to be indexed at 1
    - this "adjustment" is removed at split_tracks level, but needs to be added back when flattening tracks back into a pattern
    """
    
    def flatten(self):
        from rv.pattern import Pattern
        mods=sorted(list(self.keys()))
        index=[(mod, i)
               for mod in mods
               for i in range(self[mod].polyphony)]
        pat=Pattern(lines=self.lines,
                    tracks=len(index))
        def notefn(track, i, j):
            mod, k = index[j]
            chord=self[mod][i]
            if k < len(chord):
                note=chord[k]
                if note.module:
                    note.module+=1 # NB
                return note
            else:
                return Note()
        pat.set_via_fn(notefn)
        return pat

    def __str__(self):
        return "|".join(["%i:%s" % (mod, str(self[mod]))
                         for mod in self])

"""
- parse_timeline walks proj.patterns and replaces PatternClone references with actual Pattern data at each point in the timeline
"""
    
def parse_timeline(proj):
    from rv.pattern import PatternClone
    trackmap, timeline = {}, {}
    for i, pat in enumerate(proj.patterns):
        if (isinstance(pat, PatternClone) and
            pat.source not in trackmap):
            continue        
        if not isinstance(pat, PatternClone):
            trackmap[i]=tracks=Track.split(pat)
        else:
            tracks=trackmap[pat.source]
        if len(tracks)==0:
            continue
        timeline.setdefault(pat.x, Tracks())
        timeline[pat.x].update(tracks)
    return timeline

"""
- decompile/1 is the main entry point into the code
- firstly expands module chains and timeline
- then walks the timeline, iterates through module chains at each point in the timeline
- for each module chain, filters the subset of tracks associated with that chain
- creates a "patch" for each chain from the normalised modules for that chain, plus the tracks remapped according to `chain.mapping`
"""

def decompile(proj):
    chains=ModuleChain.expand(proj)
    timeline=parse_timeline(proj)
    cache, patches = {}, []
    for x in sorted(timeline.keys()):
        tracks=timeline[x]
        for chain in chains:
            key=str(chain)
            cache.setdefault(key, [])
            group=tracks.group(chain.modules)
            if len(group)==0:
                continue
            if (key in cache and
                str(group) in cache[key]):
                continue
            patches.append((x,
                            chain.detach(),
                            group.normalise(chain.mapping).flatten()))
            cache[key].append(str(group))
    return patches

def module_layout(n,
           seed=13,
           offset=(512, 512),
           mult=(256, 256),           
           tries=50):
    import math, random
    random.seed(seed)
    def is_neighbour(p, q):
        return (((p[0]==q[0] and
                  abs(p[1]-q[1])==1) or
                 (p[1]==q[1] and
                  abs(p[0]-q[0])==1)) and not
                ((abs(p[0]-q[0])==1)
                 and abs(p[1]-q[1])==1))
    def normalise(r):
        return [(i-r[0][0], j-r[0][1])
                for i, j in r]
    def sample(n,
               matcher=is_neighbour,
               padding=2):
        sz=padding+int(math.ceil(math.sqrt(n)))
        pairs=[(i, j)
               for i in range(sz)
               for j in range(sz)]
        q0=q=tuple([random.choice(range(sz)),
                    random.choice(range(sz))])
        pairs.remove(q)
        r=[q0]
        for i in range(n-1):
            adjacent=[p for p in pairs
                      if matcher(p, q)]
            if adjacent==[]:
                raise RuntimeError("No adjacent pairs")
            q=random.choice(adjacent)
            pairs.remove(q)
            r.append(q)
        return normalise(r)
    def div_zero(fn):
        def wrapped(r):
            if len(r)==1:
                return 1
            return fn(r)
        return wrapped
    @div_zero
    def compactness(r):
        head, tail = r[0], r[1:]
        def err(s):
            return sum([(s[i]-head[i])**2
                        for i in range(2)])
        return (sum([err(s)
                     for s in tail])/(len(r)-1))**0.5
    def best(n, tries):
        best, besterr = None, 1e10
        for i in range(tries):
            try:
                l=sample(n+1)
            except RuntimeError as error:
                continue
            err=compactness(l)
            if err < besterr:
                best, besterr = l, err
        return best[1:]
    def expand(r):
        oi, oj = offset
        mi, mj = mult
        return [(oi+mi*i, oj+mj*j)
                for i, j in r]
    return expand(best(n, tries))

"""
- dumps a patch to /tmp
"""

def dump(dirname, patch, bpm):
    x, chain, pat = patch
    from rv.api import Project
    proj=Project()
    proj.initial_bpm=bpm
    layout=module_layout(len(chain))
    for i, mod in enumerate(reversed(chain[:-1])):
        mod.x, mod.y = layout[i]
        proj.attach_module(mod)
    for i in range(len(proj.modules)-1):
        proj.connect(proj.modules[i+1],
                     proj.modules[i])
    proj.patterns.append(pat)
    def patch_filename(n=3):
        key="-".join([mod.name[:n]
                      for mod in chain
                      if not mod.name.lower().startswith("out")])
        return "tmp/%s/%s-%i.sunvox" % (dirname, key, x)
    destfilename=patch_filename()
    print (destfilename)
    from rv.lib.iff import write_chunk       
    def dump_project(project, filename):
        with open(filename, 'wb') as f:
            for name, value in project.chunks():
                if not name:
                    continue
                write_chunk(f, name, value)
    dump_project(proj, destfilename)
    
if __name__=="__main__":
    try:
        import sys, os
        if len(sys.argv) < 2:
            raise RuntimeError("Please enter filename")
        filename=sys.argv[1]
        if not os.path.exists(filename):
            raise RuntimeError("File does not exist")
        if not filename.endswith(".sunvox"):
            raise RuntimeError("File must be a .sunvox file")
        dirname=filename.split("/")[-1].split(".")[0]
        try:
            os.mkdir("tmp/%s" % dirname)
        except:
            pass
        from rv.readers.reader import read_sunvox_file
        proj=read_sunvox_file(filename)
        bpm=proj.initial_bpm
        patches=decompile(proj)
        for patch in patches:
            dump(dirname, patch, bpm)
    except RuntimeError as error:
        print ("Error: %s" % str(error))
