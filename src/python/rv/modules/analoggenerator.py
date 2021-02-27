from rv.chunks import DrawnWaveformChunk
from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.analoggenerator import BaseAnalogGenerator


class AnalogGenerator(BaseAnalogGenerator, Module):

    chnk = 2
    options_chnm = 1

    behaviors = {B.receives_notes, B.sends_audio}

    class DrawnWaveform(DrawnWaveformChunk):
        chnm = 0

    def __init__(self, **kwargs):
        samples = kwargs.pop("samples", None)
        super(AnalogGenerator, self).__init__(**kwargs)
        self.drawn_waveform = self.DrawnWaveform()
        if samples is not None:
            self.drawn_waveform.samples = samples
            print(self.drawn_waveform.samples)

    def specialized_iff_chunks(self):
        yield from super(AnalogGenerator, self).specialized_iff_chunks()
        yield from self.drawn_waveform.chunks()

    def load_chunk(self, chunk):
        if chunk.chnm == self.options_chnm:
            self.load_options(chunk)
        elif chunk.chnm == 0:
            self.load_drawn_waveform(chunk)

    def load_drawn_waveform(self, chunk):
        # Convert samples from unsigned to signed.
        self.drawn_waveform.samples = [
            (int(y) & ((1 << 7) - 1)) - (int(y) & (1 << 7)) for y in chunk.chdt
        ]
        self.drawn_waveform.format = self.drawn_waveform.Format(chunk.chff or 1)
        self.drawn_waveform.freq = chunk.chfr
