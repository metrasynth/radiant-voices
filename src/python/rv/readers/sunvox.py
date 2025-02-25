import logging
from struct import unpack
from typing import Optional

from rv import ENCODING
from rv.pattern import Pattern
from rv.project import Project
from rv.readers.module import ModuleReader
from rv.readers.pattern import PatternCloneReader, PatternReader
from rv.readers.reader import Reader, ReaderFinished

log = logging.getLogger(__name__)


class SunVoxReader(Reader):
    object: Optional[Project]

    def __init__(self, f):
        super(SunVoxReader, self).__init__(f)

    def process_chunks(self):
        self.object = Project()
        self.object.based_on_version = None
        self.object.modules.clear()
        super().process_chunks()
        if self.object.based_on_version is None:
            # Legacy SunVox files don't have a "based on" version.
            self.object.based_on_version = (1, 7, 0, 0)

    def process_VERS(self, data):
        self.object.loaded_sunvox_version = tuple(reversed(unpack("BBBB", data)))

    def process_BVER(self, data):
        self.object.based_on_version = tuple(reversed(unpack("BBBB", data)))

    def process_FLGS(self, data):
        (self.object.flags,) = unpack("<I", data)

    def process_SFGS(self, data):
        (val,) = unpack("<I", data)
        self.object.receive_sync_midi = val & 0b111
        self.object.receive_sync_other = (val >> 3) & 0b111

    def process_BPM(self, data):
        (self.object.initial_bpm,) = unpack("<I", data)

    def process_SPED(self, data):
        (self.object.initial_tpl,) = unpack("<I", data)

    def process_TGRD(self, data):
        (self.object.time_grid,) = unpack("<I", data)

    def process_TGD2(self, data):
        (self.object.time_grid2,) = unpack("<I", data)

    def process_GVOL(self, data):
        (self.object.global_volume,) = unpack("<I", data)

    def process_NAME(self, data):
        data = data[: data.find(0)] if 0 in data else data
        self.object.name = data.decode(ENCODING)

    def process_MSCL(self, data):
        (self.object.modules_scale,) = unpack("<I", data)

    def process_MZOO(self, data):
        (self.object.modules_zoom,) = unpack("<I", data)

    def process_MXOF(self, data):
        (self.object.modules_x_offset,) = unpack("<i", data)

    def process_MYOF(self, data):
        (self.object.modules_y_offset,) = unpack("<i", data)

    def process_LMSK(self, data):
        (self.object.modules_layer_mask,) = unpack("<I", data)

    def process_CURL(self, data):
        (self.object.modules_current_layer,) = unpack("<I", data)

    def process_TIME(self, data):
        (self.object.timeline_position,) = unpack("<i", data)

    def process_REPS(self, data):
        (self.object.restart_position,) = unpack("<i", data)

    def process_SELS(self, data):
        (self.object.selected_module,) = unpack("<I", data)

    def process_LGEN(self, data):
        (self.object.selected_generator,) = unpack("<i", data)

    def process_PATN(self, data):
        (self.object.current_pattern,) = unpack("<I", data)

    def process_PATT(self, data):
        (self.object.current_track,) = unpack("<I", data)

    def process_PATL(self, data):
        (self.object.current_line,) = unpack("<I", data)

    def process_PDTA(self, data):
        self.rewind(data)
        pattern = PatternReader(self.f).object
        self.object.attach_pattern(pattern)

    def process_PEND(self, data):
        # Empty pattern found.
        self.object.attach_pattern(None)

    def process_PPAR(self, data):
        self.rewind(data)
        pattern = PatternCloneReader(self.f).object
        self.object.attach_pattern(pattern)

    def process_SFFF(self, data):
        self.rewind(data)
        index = len(self.object.modules)
        reader = ModuleReader(self.f, index=index)
        reader.process_chunks()
        mod = reader.object
        self.object.attach_module(mod, loading=True)

    def process_SEND(self, _):
        self.object.attach_module(None, loading=True)  # empty module

    def process_end_of_file(self):
        # Clear out empty modules at end of list.
        while self.object.modules and self.object.modules[-1] is None:
            self.object.modules.pop()
        # inLinkSlots are not written out by SunVox if all zeros; initialize if missing.
        # Start with the first non-output module, work our way up, then output module.
        for mod in self.object.modules[1:] + self.object.modules[:1]:
            if not mod or mod.in_link_slots:
                continue
            for other_mod_num in mod.in_links:
                if other_mod_num == -1:
                    mod.in_link_slots.append(-1)
                    continue
                if other_mod_num >= len(self.object.modules):
                    log.warning(
                        "Found SLNK on %r referencing non-existent module %r",
                        mod.index,
                        other_mod_num,
                    )
                    continue
                other_mod = self.object.modules[other_mod_num]
                in_slot = len(other_mod.out_link_slots)
                out_slot = len(mod.in_link_slots)
                mod.in_link_slots.append(in_slot)
                other_mod.out_links.append(mod.index)
                other_mod.out_link_slots.append(out_slot)
        # generate outLinks based on inLinks
        for mod in self.object.modules:
            if not mod:
                continue
            in_links = mod.in_links
            in_link_slots = mod.in_link_slots
            for in_link_idx, in_link in enumerate(in_links):
                out_link_idx = in_link_slots[in_link_idx]
                src_mod = self.object.modules[in_link]
                if not src_mod:
                    raise RuntimeError()
                out_links = src_mod.out_links
                out_link_slots = src_mod.out_link_slots
                while out_link_idx >= len(out_links):
                    out_links.append(-1)
                while out_link_idx >= len(out_link_slots):
                    out_link_slots.append(-1)
                if out_link_idx != -1:
                    out_links[out_link_idx] = mod.index
                    out_link_slots[out_link_idx] = in_link_idx
        # Clear high byte of module in patterns if version was < 1.9.5.0
        if self.object.loaded_sunvox_version < (1, 9, 5, 0):
            for pat in self.object.patterns:
                if not isinstance(pat, Pattern):
                    continue
                for line in pat.data:
                    for note in line:
                        note.module &= 0xFF
        raise ReaderFinished()
