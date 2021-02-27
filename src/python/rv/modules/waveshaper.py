from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.waveshaper import BaseWaveShaper


class WaveShaper(BaseWaveShaper, Module):

    chnk = 1

    behaviors = {B.receives_audio, B.sends_audio}

    def __init__(self, **kwargs):
        values = kwargs.pop("values", None)
        super(WaveShaper, self).__init__(**kwargs)
        self.curve = self.curve_chunk()
        if values is not None:
            self.curve.values = values

    def specialized_iff_chunks(self):
        yield from self.curve.chunks()
        yield from super(WaveShaper, self).specialized_iff_chunks()

    def load_chunk(self, chunk):
        if chunk.chnm == 0:
            self.curve.bytes = chunk.chdt
