from rv.chunks import DirtyWaveformChunk
from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.generator import BaseGenerator


class Generator(BaseGenerator, Module):

    chnk = 1

    behaviors = {B.receives_notes, B.receives_modulator, B.sends_audio}

    class DirtyWaveform(DirtyWaveformChunk):
        chnm = 0

    def __init__(self, **kwargs):
        samples = kwargs.pop("samples", None)
        super(Generator, self).__init__(**kwargs)
        self.dirty_waveform = self.DirtyWaveform()
        if samples is not None:
            self.dirty_waveform.samples = samples

    def specialized_iff_chunks(self):
        yield from self.dirty_waveform.chunks()
        yield from super(Generator, self).specialized_iff_chunks()

    def load_chunk(self, chunk):
        if chunk.chnm == 0:
            self.load_dirty_waveform(chunk)

    def load_dirty_waveform(self, chunk):
        self.dirty_waveform.samples = chunk.chdt
        self.dirty_waveform.format = self.dirty_waveform.Format(chunk.chff or 1)
        self.dirty_waveform.freq = chunk.chfr
