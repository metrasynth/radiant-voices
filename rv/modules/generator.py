from rv.chunks import DirtyWaveformChunk
from rv.controller import Controller
from rv.modules import Behavior as B, Module
from rv.modules.base.generator import BaseGenerator


class Generator(BaseGenerator, Module):

    chnk = 1
    flags = 0x000059

    behaviors = {B.receives_notes, B.receives_modulator, B.sends_audio}

    Waveform = BaseGenerator.Waveform
    Mode = BaseGenerator.Mode

    class DirtyWaveform(DirtyWaveformChunk):
        chnm = 0

    volume = Controller((0, 256), 128)
    waveform = Controller(Waveform, Waveform.triangle)
    panning = Controller((-128, 128), 0)
    attack = Controller((0, 512), 0)
    release = Controller((0, 512), 0)
    polyphony_ch = Controller((1, 16), 8)
    mode = Controller(Mode, Mode.stereo)
    sustain = Controller(bool, True)
    freq_modulation_input = Controller((0, 256), 0)
    duty_cycle = Controller((0, 1022), 511)

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
