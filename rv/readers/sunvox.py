from struct import unpack

from rv import ENCODING
from rv.project import Project
from rv.readers.module import ModuleReader
from rv.readers.pattern import PatternCloneReader, PatternReader
from rv.readers.reader import Reader, ReaderFinished


class SunVoxReader(Reader):
    def __init__(self, f):
        super(SunVoxReader, self).__init__(f)

    def process_chunks(self):
        self.object = Project()
        self.object.modules.clear()
        super().process_chunks()

    def process_VERS(self, data):
        self.object.sunvox_version = tuple(reversed(unpack("BBBB", data)))

    def process_BVER(self, data):
        self.object.based_on_version = tuple(reversed(unpack("BBBB", data)))

    def process_BPM(self, data):
        self.object.initial_bpm, = unpack("<I", data)

    def process_SPED(self, data):
        self.object.initial_tpl, = unpack("<I", data)

    def process_TGRD(self, data):
        self.object.time_grid, = unpack("<I", data)

    def process_TGD2(self, data):
        self.object.time_grid2, = unpack("<I", data)

    def process_GVOL(self, data):
        self.object.global_volume, = unpack("<I", data)

    def process_NAME(self, data):
        data = data[: data.find(0)] if 0 in data else data
        self.object.name = data.decode(ENCODING)

    def process_MSCL(self, data):
        self.object.modules_scale, = unpack("<I", data)

    def process_MZOO(self, data):
        self.object.modules_zoom, = unpack("<I", data)

    def process_MXOF(self, data):
        self.object.modules_x_offset, = unpack("<i", data)

    def process_MYOF(self, data):
        self.object.modules_y_offset, = unpack("<i", data)

    def process_LMSK(self, data):
        self.object.modules_layer_mask, = unpack("<I", data)

    def process_CURL(self, data):
        self.object.modules_current_layer, = unpack("<I", data)

    def process_TIME(self, data):
        self.object.timeline_position, = unpack("<i", data)

    def process_REPS(self, data):
        self.object.restart_position, = unpack("<i", data)

    def process_SELS(self, data):
        self.object.selected_module, = unpack("<I", data)

    def process_LGEN(self, data):
        self.object.selected_generator, = unpack("<I", data)

    def process_PATN(self, data):
        self.object.current_pattern, = unpack("<I", data)

    def process_PATT(self, data):
        self.object.current_track, = unpack("<I", data)

    def process_PATL(self, data):
        self.object.current_line, = unpack("<I", data)

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
        mod = ModuleReader(self.f, index=len(self.object.modules)).object
        self.object.attach_module(mod)

    def process_SEND(self, _):
        self.object.attach_module(None)  # empty module

    def process_end_of_file(self):
        # Clear out empty modules at end of list.
        while self.object.modules[-1:] == [None]:
            self.object.modules.pop()
        raise ReaderFinished()
