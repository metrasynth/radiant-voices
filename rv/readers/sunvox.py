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

    def process_vers(self, data):
        self.object.sunvox_version = tuple(reversed(unpack('BBBB', data)))

    def process_bver(self, data):
        self.object.based_on_version = tuple(reversed(unpack('BBBB', data)))

    def process_bpm(self, data):
        self.object.initial_bpm, = unpack('<I', data)

    def process_sped(self, data):
        self.object.initial_tpl, = unpack('<I', data)

    def process_tgrd(self, data):
        self.object.time_grid, = unpack('<I', data)

    def process_gvol(self, data):
        self.object.global_volume, = unpack('<I', data)

    def process_name(self, data):
        data = data[:data.find(0)] if 0 in data else data
        self.object.name = data.decode(ENCODING)

    def process_mscl(self, data):
        self.object.modules_scale, = unpack('<I', data)

    def process_mzoo(self, data):
        self.object.modules_zoom, = unpack('<I', data)

    def process_mxof(self, data):
        self.object.modules_x_offset, = unpack('<i', data)

    def process_myof(self, data):
        self.object.modules_y_offset, = unpack('<i', data)

    def process_lmsk(self, data):
        self.object.modules_layer_mask, = unpack('<I', data)

    def process_curl(self, data):
        self.object.modules_current_layer, = unpack('<I', data)

    def process_time(self, data):
        self.object.timeline_position, = unpack('<i', data)

    def process_sels(self, data):
        self.object.selected_module, = unpack('<I', data)

    def process_lgen(self, data):
        self.object._reader_lgen = data

    def process_patn(self, data):
        self.object.current_pattern, = unpack('<I', data)

    def process_patt(self, data):
        self.object.current_track, = unpack('<I', data)

    def process_patl(self, data):
        self.object.current_line, = unpack('<I', data)

    def process_pdta(self, data):
        self.rewind(data)
        pattern = PatternReader(self.f).object
        self.object.attach_pattern(pattern)

    def process_pend(self, data):
        # Empty pattern found.
        self.object.attach_pattern(None)

    def process_ppar(self, data):
        self.rewind(data)
        pattern = PatternCloneReader(self.f).object
        self.object.attach_pattern(pattern)

    def process_sfff(self, data):
        self.rewind(data)
        module = ModuleReader(self.f, index=len(self.object.modules)).object
        self.object.attach_module(module)

    def process_send(self, _):
        self.object.attach_module(None)  # empty module

    def process_end_of_file(self):
        # Clear out empty modules at end of list.
        while self.object.modules[-1:] == [None]:
            self.object.modules.pop()
        raise ReaderFinished()
