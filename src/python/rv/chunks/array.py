from struct import pack, unpack

from .chunk import Chunk


class ArrayChunk(Chunk):
    length = None
    element_size = None
    type = None
    python_type = int
    default = None
    values = None
    min_value = None
    max_value = None

    def __init__(self):
        self.reset()

    @property
    def bytes(self):
        return pack("<" + self.type * self.length, *self.encoded_values)

    @bytes.setter
    def bytes(self, value):
        self._set_bytes(value)

    def _set_bytes(self, value):
        self.values = []
        length = len(value) // self.element_size
        for x in range(length):
            start = x * self.element_size
            end = start + self.element_size
            data = value[start:end]
            unpacked = unpack(f"<{self.type}", data)
            if len(unpacked) == 1:
                (unpacked,) = unpacked
            actual = self.python_type(unpacked)
            self.values.append(actual)

    @property
    def encoded_values(self):
        return self.values

    def chdt(self):
        return self.bytes

    def reset(self):
        if self.default is None:
            self.values = [0] * self.length

        elif callable(self.default):
            self.set_via_fn(self.default)
        elif isinstance(self.default, list):
            self.values = self.default.copy()
        else:
            self.values = [self.default] * self.length

    def set_via_fn(self, fn):
        values = []
        for x in range(self.length):
            y = fn(x)
            if self.min_value:
                y = max(y, self.min_value)
            if self.max_value:
                y = min(y, self.max_value)
            values.append(y)
        self.values = values


__all__ = ["ArrayChunk"]
