from struct import pack, unpack

from .chunk import Chunk


class ArrayChunk(Chunk):

    length = None
    type = None
    default = None
    values = None

    def __init__(self):
        if self.default is not None:
            self.values = self.default.copy()
        else:
            self.values = [0] * self.length

    @property
    def bytes(self):
        return pack('<' + self.type * self.length, *self.values)

    @bytes.setter
    def bytes(self, value):
        self.values = unpack('<' + self.type * self.length, value)

    def chdt(self):
        return self.bytes

    def chff(self):
        return pack('<I', 0)

    def chfr(self):
        return pack('<I', 0)


__all__ = [
    'ArrayChunk',
]
