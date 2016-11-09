import logging
from struct import unpack

from rv import ENCODING
from rv.pattern import Pattern, PatternClone
from rv.readers.reader import Reader, ReaderFinished

log = logging.getLogger(__name__)


class PatternReader(Reader):

    def process_pdta(self, data):
        self.object = Pattern()
        # Don't set directly on pattern;
        # we don't yet have tracks and lines.
        self._raw_data = data

    def process_pnme(self, data):
        data = data[:data.find(0)] if 0 in data else data
        self.object.name = data.decode(ENCODING)

    def process_pchn(self, data):
        self.object.tracks, = unpack('<I', data)

    def process_plin(self, data):
        self.object.lines, = unpack('<I', data)

    def process_pysz(self, data):
        self.object.y_size, = unpack('<I', data)

    def process_pflg(self, data):
        self.object.appearance_flags, = unpack('<I', data)

    def process_pico(self, data):
        self.object.icon = data

    def process_pfgc(self, data):
        self.object.fg_color = unpack('<BBB', data)

    def process_pbgc(self, data):
        self.object.bg_color = unpack('<BBB', data)

    def process_pfff(self, data):
        self.object.flags, = unpack('<I', data)

    def process_pxxx(self, data):
        self.object.x, = unpack('<i', data)

    def process_pyyy(self, data):
        self.object.y, = unpack('<i', data)

    def process_pend(self, data):
        # We now have tracks and lines,
        # so we can now set raw_data on the pattern.
        self.object.raw_data = self._raw_data
        raise ReaderFinished()


class PatternCloneReader(Reader):

    def process_ppar(self, data):
        source, = unpack('<I', data)
        self.object = PatternClone(source=source)

    def process_pfff(self, data):
        self.object.flags, = unpack('<I', data)

    def process_pxxx(self, data):
        self.object.x, = unpack('<i', data)

    def process_pyyy(self, data):
        self.object.y, = unpack('<i', data)

    def process_pend(self, data):
        raise ReaderFinished()
