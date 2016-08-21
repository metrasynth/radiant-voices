import logging

from logutils import BraceMessage as _F

log = logging.getLogger(__name__)

from struct import unpack

from rv import ENCODING
from rv.modules import MODULE_CLASSES, Module
from rv.modules.output import OutputModule
from rv.readers.reader import Reader, ReaderFinished


class ModuleReader(Reader):

    def __init__(self, f, index):
        super(ModuleReader, self).__init__(f)
        self._index = index
        self._current_controller = 0

    def process_chunks(self):
        if self._index > 0:
            self.object = Module()
        else:
            self.object = OutputModule()
        super().process_chunks()

    def process_sfff(self, data):
        self.object.flags, = unpack('<I', data)

    def process_snam(self, data):
        self.object.name = data.rstrip(b'\0').decode(ENCODING)

    def process_styp(self, data):
        mtype = data.rstrip(b'\0').decode(ENCODING)
        cls = MODULE_CLASSES[mtype]
        new_module = cls()
        new_module.flags = self.object.flags
        new_module.name = self.object.name
        new_module.mtype = mtype
        self._controller_keys = list(new_module.controllers.keys())
        self._object = new_module

    def process_sfin(self, data):
        self.object.finetune, = unpack('<i', data)

    def process_srel(self, data):
        self.object.relative_note, = unpack('<i', data)

    def process_sxxx(self, data):
        self.object.x_position, = unpack('<i', data)

    def process_syyy(self, data):
        self.object.y_position, = unpack('<i', data)

    def process_szzz(self, data):
        self.object.layer, = unpack('<I', data)

    def process_sscl(self, data):
        self.object.scale, = unpack('<I', data)

    def process_svpr(self, data):
        self.object.visualization, = unpack('<I', data)

    def process_scol(self, data):
        self.object.color = unpack('BBB', data)

    def process_smic(self, data):
        self.object.midi_out_channel, = unpack('<i', data)

    def process_smib(self, data):
        self.object.midi_out_bank, = unpack('<i', data)

    def process_smip(self, data):
        self.object.midi_out_program, = unpack('<i', data)

    def process_slnk(self, data):
        links = self.object.incoming_links
        if len(data) > 0:
            link_count = len(data) // 4
            structure = '<' + 'i' * link_count
            links.extend(unpack(structure, data))
            if links[-1] == -1:
                links.pop()

    def process_cval(self, data):
        raw_value, = unpack('<i', data)
        if self._current_controller < len(self._controller_keys):
            controller_name = self._controller_keys[self._current_controller]
            self.object.set_raw(controller_name, raw_value)
        else:
            log.warn(_F('Unsupported controller at index {} with raw value {}',
                        self._current_controller, raw_value))
        self._current_controller += 1

    def process_send(self, data):
        raise ReaderFinished()
