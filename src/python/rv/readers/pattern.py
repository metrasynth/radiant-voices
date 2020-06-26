import logging
from struct import unpack

from rv import ENCODING
from rv.pattern import Pattern, PatternClone
from rv.readers.reader import Reader, ReaderFinished

log = logging.getLogger(__name__)


class PatternReader(Reader):
    def process_PDTA(self, data):
        self.object = Pattern()
        # Don't set directly on pattern;
        # we don't yet have tracks and lines.
        self._raw_data = data

    def process_PNME(self, data):
        data = data[: data.find(0)] if 0 in data else data
        self.object.name = data.decode(ENCODING)

    def process_PCHN(self, data):
        (self.object.tracks,) = unpack("<I", data)

    def process_PLIN(self, data):
        (self.object.lines,) = unpack("<I", data)

    def process_PYSZ(self, data):
        (self.object.y_size,) = unpack("<I", data)

    def process_PFLG(self, data):
        (self.object.appearance_flags,) = unpack("<I", data)

    def process_PICO(self, data):
        self.object.icon = data

    def process_PFGC(self, data):
        self.object.fg_color = unpack("<BBB", data)

    def process_PBGC(self, data):
        self.object.bg_color = unpack("<BBB", data)

    def process_PFFF(self, data):
        (self.object.flags,) = unpack("<I", data)

    def process_PXXX(self, data):
        (self.object.x,) = unpack("<i", data)

    def process_PYYY(self, data):
        (self.object.y,) = unpack("<i", data)

    def process_PSYN(self, data):
        pass  # Unused in current SunVox.

    def process_PCTL(self, data):
        pass  # Unused in current SunVox.

    def process_PEND(self, data):
        # We now have tracks and lines,
        # so we can now set raw_data on the pattern.
        self.object.raw_data = self._raw_data
        raise ReaderFinished()


class PatternCloneReader(Reader):
    def process_PPAR(self, data):
        (source,) = unpack("<I", data)
        self.object = PatternClone(source=source)

    def process_PFFF(self, data):
        (self.object.flags,) = unpack("<I", data)

    def process_PXXX(self, data):
        (self.object.x,) = unpack("<i", data)

    def process_PYYY(self, data):
        (self.object.y,) = unpack("<i", data)

    def process_PEND(self, data):
        raise ReaderFinished()
