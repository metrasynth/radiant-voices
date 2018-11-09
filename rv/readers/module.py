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
        self._current_chunk = None
        self._cvals = []

    def process_chunks(self):
        if self._index > 0:
            self.object = Module(index=self._index)
        else:
            self.object = Output()
        super().process_chunks()

    def process_sfff(self, data):
        self.object.flags, = unpack("<I", data)

    def process_snam(self, data):
        data = data[: data.find(0)] if 0 in data else data
        self.object.name = data.decode(ENCODING)

    def process_styp(self, data):
        data = data[: data.find(0)] if 0 in data else data
        mtype = data.decode(ENCODING)
        cls = MODULE_CLASSES[mtype]
        new_module = cls()
        new_module.flags = self.object.flags
        new_module.name = self.object.name
        new_module.mtype = mtype
        self._controller_keys = list(
            name
            for name, controller in new_module.controllers.items()
            if controller.attached(new_module)
        )
        if mtype == "MetaModule":
            self._controller_keys += [
                "user_defined_{}".format(i + 1) for i in range(27)
            ]
        self._object = new_module

    def process_sfin(self, data):
        self.object.finetune, = unpack("<i", data)

    def process_srel(self, data):
        self.object.relative_note, = unpack("<i", data)

    def process_sxxx(self, data):
        self.object.x, = unpack("<i", data)

    def process_syyy(self, data):
        self.object.y, = unpack("<i", data)

    def process_szzz(self, data):
        self.object.layer, = unpack("<I", data)

    def process_sscl(self, data):
        self.object.scale, = unpack("<I", data)

    def process_svpr(self, data):
        self.object.visualization, = unpack("<I", data)

    def process_scol(self, data):
        self.object.color = unpack("BBB", data)

    def process_smii(self, data):
        x, = unpack("<I", data)
        self.object.midi_in_always = bool(x & 1)
        self.object.midi_in_channel = x >> 1

    def process_smin(self, data):
        data = data[: data.find(0)] if 0 in data else data
        self.object.midi_out_name = data.decode(ENCODING)

    def process_smic(self, data):
        self.object.midi_out_channel, = unpack("<i", data)

    def process_smib(self, data):
        self.object.midi_out_bank, = unpack("<i", data)

    def process_smip(self, data):
        self.object.midi_out_program, = unpack("<i", data)

    def process_slnk(self, data):
        links = self.object.incoming_links
        if len(data) > 0:
            link_count = len(data) // 4
            structure = "<" + "i" * link_count
            links.extend(unpack(structure, data))
            while links[-1:] == [-1]:
                links.pop()

    def process_cval(self, data):
        raw_value, = unpack("<i", data)
        self._cvals.append(raw_value)

    def _load_last_chunk(self):
        if self._current_chunk:
            self.object.load_chunk(self._current_chunk)
            self._current_chunk = None

    def process_chnk(self, data):
        val, = unpack("<I", data)
        self.object._reader_chnk = val

    def process_chnm(self, data):
        self._load_last_chunk()
        self._current_chunk = Chunk()
        self._current_chunk.chnm, = unpack("<I", data)

    def process_chdt(self, data):
        self._current_chunk.chdt = data

    def process_chff(self, data):
        self._current_chunk.chff, = unpack("<I", data)

    def process_chfr(self, data):
        self._current_chunk.chfr, = unpack("<I", data)

    def process_cmid(self, data):
        self.object.load_cmid(data)

    def process_send(self, data):
        self._load_last_chunk()
        self.object.finalize_load()
        if self.object.mtype == "MetaModule":
            self.object.update_user_defined_controllers()
            self.object.recompute_controller_attachment()
        for cnum, raw_value in reversed(list(enumerate(self._cvals))):
            if cnum < len(self._controller_keys):
                controller_name = self._controller_keys[cnum]
                log.debug(_F("Setting {} from raw {}", controller_name, raw_value))
                self.object.set_raw(controller_name, raw_value)
                self.object.controllers_loaded.add(controller_name)
            else:
                log.warning(
                    _F(
                        "Unsupported controller at index {} with raw value {}",
                        cnum,
                        raw_value,
                    )
                )
        raise ReaderFinished()
