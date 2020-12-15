from __future__ import annotations

import logging
from struct import unpack

from logutils import BraceMessage as _F
from rv import ENCODING
from rv.modules import MODULE_CLASSES, Chunk, Module
from rv.modules.metamodule import MetaModule
from rv.modules.output import Output
from rv.readers.reader import Reader, ReaderFinished

log = logging.getLogger(__name__)


class ModuleReader(Reader):

    object: Module

    def __init__(self, f, index):
        super(ModuleReader, self).__init__(f)
        self._index = index
        self._current_chunk = None
        self._cvals = []

    def process_chunks(self):
        self.object = Module(index=self._index) if self._index > 0 else Output()
        super().process_chunks()

    def process_SFFF(self, data):
        (self.object.flags,) = unpack("<I", data)

    def process_SNAM(self, data):
        data = data[: data.find(0)] if 0 in data else data
        self.object.name = data.decode(ENCODING)

    def process_STYP(self, data):
        data = data[: data.find(0)] if 0 in data else data
        mtype = data.decode(ENCODING)
        cls = MODULE_CLASSES[mtype]
        new_module = cls()
        new_module.flags = self.object.flags
        new_module.name = self.object.name
        new_module.mtype = mtype
        self._controller_keys = [
            name
            for name, controller in new_module.controllers.items()
            if controller.attached(new_module)
        ]

        if mtype == "MetaModule":
            self._controller_keys += [
                "user_defined_{}".format(i + 1) for i in range(27)
            ]
        self._object = new_module

    def process_SFIN(self, data):
        (self.object.finetune,) = unpack("<i", data)

    def process_SREL(self, data):
        (self.object.relative_note,) = unpack("<i", data)

    def process_SXXX(self, data):
        (self.object.x,) = unpack("<i", data)

    def process_SYYY(self, data):
        (self.object.y,) = unpack("<i", data)

    def process_SZZZ(self, data):
        (self.object.layer,) = unpack("<I", data)

    def process_SSCL(self, data):
        (self.object.scale,) = unpack("<I", data)

    def process_SVPR(self, data):
        (self.object.visualization,) = unpack("<I", data)

    def process_SCOL(self, data):
        self.object.color = unpack("BBB", data)

    def process_SMII(self, data):
        (x,) = unpack("<I", data)
        self.object.midi_in_always = bool(x & 1)
        self.object.midi_in_channel = x >> 1

    def process_SMIN(self, data):
        data = data[: data.find(0)] if 0 in data else data
        self.object.midi_out_name = data.decode(ENCODING)

    def process_SMIC(self, data):
        (self.object.midi_out_channel,) = unpack("<i", data)

    def process_SMIB(self, data):
        (self.object.midi_out_bank,) = unpack("<i", data)

    def process_SMIP(self, data):
        (self.object.midi_out_program,) = unpack("<i", data)

    def process_SLNK(self, data):
        if len(data) > 0:
            link_count = len(data) // 4
            structure = "<" + "i" * link_count
            links = self.object.in_links
            links.extend(unpack(structure, data))
            while links[-1:] == [-1]:
                links.pop()

    def process_SLnK(self, data):
        if len(data) > 0:
            link_count = len(data) // 4
            structure = "<" + "i" * link_count
            slots = self.object.in_link_slots
            slots.extend(unpack(structure, data))
            while slots[-1:] == [-1]:
                slots.pop()

    def process_CVAL(self, data):
        (raw_value,) = unpack("<i", data)
        self._cvals.append(raw_value)

    def _load_last_chunk(self):
        if self._current_chunk:
            self.object.load_chunk(self._current_chunk)
            self._current_chunk = None

    def process_CHNK(self, data):
        (val,) = unpack("<I", data)
        self.object._reader_chnk = val

    def process_CHNM(self, data):
        self._load_last_chunk()
        self._current_chunk = Chunk()
        (self._current_chunk.chnm,) = unpack("<I", data)

    def process_CHDT(self, data):
        self._current_chunk.chdt = data

    def process_CHFF(self, data):
        (self._current_chunk.chff,) = unpack("<I", data)

    def process_CHFR(self, data):
        (self._current_chunk.chfr,) = unpack("<I", data)

    def process_CMID(self, data):
        self.object.load_cmid(data)

    def process_SEND(self, data):
        self._load_last_chunk()
        self.object.finalize_load()
        if isinstance(self.object, MetaModule):
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
