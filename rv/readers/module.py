import logging
from struct import unpack

from logutils import BraceMessage as _F

from rv import ENCODING
from rv.modules import MODULE_CLASSES, Chunk, Module
from rv.modules.output import Output
from rv.readers.reader import Reader, ReaderFinished

log = logging.getLogger(__name__)


class ModuleReader(Reader):

    def __init__(self, f, index):
        super(ModuleReader, self).__init__(f)
        self._index = index
        self._current_controller = 0
        self._current_chunk = None

    def process_chunks(self):
        if self._index > 0:
            self.object = Module()
        else:
            self.object = Output()
        super().process_chunks()

    def process_sfff(self, data):
        self.object.flags, = unpack('<I', data)

    def process_snam(self, data):
        data = data[:data.find(0)] if 0 in data else data
        self.object.name = data.decode(ENCODING)

    def process_styp(self, data):
        data = data[:data.find(0)] if 0 in data else data
        mtype = data.decode(ENCODING)
        cls = MODULE_CLASSES[mtype]
        new_module = cls()
        new_module.flags = self.object.flags
        new_module.name = self.object.name
        new_module.mtype = mtype
        self._controller_keys = list(
            name for name, controller in new_module.controllers.items()
            if controller.attached(new_module)
        )
        if mtype == 'MetaModule':
            self._controller_keys += [
                'user_defined_{}'.format(i + 1)
                for i in range(27)
            ]
        self._object = new_module

    def process_sfin(self, data):
        self.object.finetune, = unpack('<i', data)

    def process_srel(self, data):
        self.object.relative_note, = unpack('<i', data)

    def process_sxxx(self, data):
        self.object.x, = unpack('<i', data)

    def process_syyy(self, data):
        self.object.y, = unpack('<i', data)

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
            log.debug(_F('Setting {} from raw {}', controller_name, raw_value))
            self.object.set_raw(controller_name, raw_value)
        else:
            log.warn(_F('Unsupported controller at index {} with raw value {}',
                        self._current_controller, raw_value))
        self._current_controller += 1

    def process_chnk(self, data):
        val, = unpack('<I', data)
        self.object._reader_chnk = val

    def process_chnm(self, data):
        self._compensate_for_older_sunvox_file_format()
        self._current_chunk = Chunk()
        self._current_chunk.chnm, = unpack('<I', data)

    def process_chdt(self, data):
        self._current_chunk.chdt = data

    def process_chff(self, data):
        self._current_chunk.chff, = unpack('<I', data)

    def process_chfr(self, data):
        self._current_chunk.chfr, = unpack('<I', data)
        self.object.load_chunk(self._current_chunk)
        self._current_chunk = None

    def process_cmid(self, data):
        self.object.load_cmid(data)

    def process_send(self, data):
        self._compensate_for_older_sunvox_file_format()
        if hasattr(self.object, '_reader_chnk'):
            chnk = self.object._reader_chnk
            expected_chnk = max(0x10, self.object.chnk)
            if chnk != expected_chnk:
                log.warn(_F('{} expected CHNK {}, got {}',
                            self.object, expected_chnk, chnk))
        raise ReaderFinished()

    def _compensate_for_older_sunvox_file_format(self):
        if self._current_chunk is not None:
            # Compensate for older versions of SunVox that didn't write
            # CHFF and CHFR for all types of chunks.
            c = self._current_chunk
            c.chff = 0 if c.chff is None else c.chff
            c.chfr = 0 if c.chfr is None else c.chfr
            self.object.load_chunk(c)
            self._current_chunk = None
