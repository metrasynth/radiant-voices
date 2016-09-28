from enum import Enum
from struct import pack

from .chunk import Chunk


class WaveformChunk(Chunk):

    class Format(Enum):
        unknown = 0x00
        mono_8bit = 0x01
        mono_16bit = 0x02
        mono_32bit = 0x04
        stereo_8bit = 0x09
        stereo_16bit = 0x0a
        stereo_32bit = 0x0c

    fixed_length = None
    fixed_format = None
    fixed_freq = None

    default = None
    format = None
    freq = None

    def __init__(self):
        if self.fixed_format is not None:
            self.format = self.fixed_format
        if self.fixed_freq is not None:
            self.freq = self.fixed_freq
        if self.default is not None:
            self.samples = self.default.copy()
        else:
            self.samples = []

    @property
    def bytes(self):
        if self.format in [self.Format.mono_8bit, self.Format.unknown]:
            return bytes(self.samples)
        else:
            raise NotImplementedError()

    def chdt(self):
        return self.bytes

    def chff(self):
        return pack('<I', self.format.value)

    def chfr(self):
        return pack('<I', self.freq)


__all__ = [
    'WaveformChunk',
]
