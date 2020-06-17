from rv.chunks import ArrayChunk
from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.waveshaper import BaseWaveShaper


class WaveShaper(BaseWaveShaper, Module):

    chnk = 1
    flags = 0x000051

    behaviors = {B.receives_audio, B.sends_audio}

    class Curve(ArrayChunk):
        chnm = 0
        length = 256
        type = "H"
        element_size = 2
        min_value = 0
        max_value = 0xFFFF

        def default(self, x):
            return x * 0x100

    def __init__(self, **kwargs):
        values = kwargs.pop("values", None)
        super(WaveShaper, self).__init__(**kwargs)
        self.curve = self.Curve()
        if values is not None:
            self.curve.values = values

    def specialized_iff_chunks(self):
        yield from self.curve.chunks()
        yield from super(WaveShaper, self).specialized_iff_chunks()

    def load_chunk(self, chunk):
        if chunk.chnm == 0:
            self.curve.bytes = chunk.chdt
