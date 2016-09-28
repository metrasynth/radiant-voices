from struct import pack, unpack

from .chunk import Chunk


class ArrayChunk(Chunk):

    length = None
    element_size = None
    type = None
    python_type = int
    default = None
    values = None

    def __init__(self):
        if self.default is not None:
            self.values = self.default.copy()
        else:
            self.values = [0] * self.length

    @property
    def bytes(self):
        return pack('<' + self.type * self.length, *self.encoded_values)

    @bytes.setter
    def bytes(self, value):
        self.values = []
        for x in range(self.length):
            start = x * self.element_size
            end = start + self.element_size
            data = value[start:end]
            unpacked = unpack('<' + self.type, data)
            if len(unpacked) == 1:
                unpacked, = unpacked
            actual = self.python_type(unpacked)
            self.values.append(actual)

    @property
    def encoded_values(self):
        return self.values

    def chdt(self):
        return self.bytes

    def chff(self):
        return pack('<I', 0)

    def chfr(self):
        return pack('<I', 0)


__all__ = [
    'ArrayChunk',
]