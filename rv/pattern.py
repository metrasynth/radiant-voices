from struct import pack

from attr import attr, attributes

from rv import ENCODING
from rv.lib.validators import divisible_by, in_range, is_length
from rv.note import Note


@attributes
class Pattern(object):

    name = attr(None)
    tracks = attr(validator=in_range(1, 16), default=4)
    lines = attr(validator=in_range(4, 4096), default=32)
    y_size = attr(default=32)
    appearance_flags = attr(default=0x00000000)
    icon = attr(default=b'\0' * 32, validator=is_length(32))
    fg_color = attr(default=(0, 0, 0))
    bg_color = attr(default=(255, 255, 255))
    flags = attr(default=0x00000000)
    x = attr(default=0, validator=divisible_by(4))
    y = attr(default=0, validator=divisible_by(4))

    @property
    def data(self):
        if not hasattr(self, '_data'):
            self._init_data()
        return self._data

    @property
    def raw_data(self):
        return b''.join(
            b''.join(note.raw_data for note in line)
            for line in self.data
        )

    @raw_data.setter
    def raw_data(self, raw_data):
        data = self.data
        for line_no in range(self.lines):
            for track_no in range(self.tracks):
                offset = (line_no * self.tracks * 8) + (track_no * 8)
                note_raw_data = raw_data[offset:offset+8]
                data[line_no][track_no].raw_data = note_raw_data

    def iff_chunks(self):
        yield (b'PDTA', self.raw_data)
        if self.name is not None:
            yield (b'PNME', self.name.encode(ENCODING) + b'\0')
        yield (b'PCHN', pack('<I', self.tracks))
        yield (b'PLIN', pack('<I', self.lines))
        yield (b'PYSZ', pack('<I', self.y_size))
        yield (b'PFLG', pack('<I', self.appearance_flags))
        yield (b'PICO', self.icon)
        yield (b'PFGC', pack('<BBB', *self.fg_color))
        yield (b'PBGC', pack('<BBB', *self.bg_color))
        yield (b'PFFF', pack('<I', self.flags))
        yield (b'PXXX', pack('<i', self.x))
        yield (b'PYYY', pack('<i', self.y))

    def _init_data(self):
        self._data = []
        for line_no in range(self.lines):
            line = []
            self._data.append(line)
            for track_no in range(self.tracks):
                line.append(Note())

    def tabular_repr(self):
        return '\n'.join(
            ' '.join(note.tabular_repr() for note in line)
            for line in self.data
        )


@attributes
class PatternClone(object):

    source = attr()
    flags = attr(default=0x00000001)
    x = attr(default=0, validator=divisible_by(4))
    y = attr(default=0, validator=divisible_by(4))

    def iff_chunks(self):
        yield (b'PPAR', pack('<I', self.source))
        yield (b'PFFF', pack('<I', self.flags))
        yield (b'PXXX', pack('<i', self.x))
        yield (b'PYYY', pack('<i', self.y))
