from enum import Enum

from rv.chunks import DirtyWaveformChunk
from rv.controller import Controller
from rv.modules import Behavior as B, Module


class Generator(Module):

    name = mtype = 'Generator'
    mgroup = 'Synth'
    chnk = 0x10

    behaviors = {B.receives_notes, B.receives_modulator, B.sends_audio}

    class Waveform(Enum):
        triangle = 0
        saw = 1
        square = 2
        noise = 3
        dirty = 4
        sin = 5
        hsin = 6
        asin = 7
        psin = 8

    class Mode(Enum):
        stereo = 0
        mono = 1

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
        samples = kwargs.pop('samples', None)
        super(Generator, self).__init__(**kwargs)
        self.dirty_waveform = self.DirtyWaveform()
        if samples is not None:
            self.dirty_waveform.samples = samples

    def specialized_iff_chunks(self):
        for chunk in self.dirty_waveform.chunks():
            yield chunk
        for chunk in super(Generator, self).specialized_iff_chunks():
            yield chunk

    def load_chunk(self, chunk):
        if chunk.chnm == 0:
            self.load_dirty_waveform(chunk)

    def load_dirty_waveform(self, chunk):
        self.dirty_waveform.samples = chunk.chdt
        self.dirty_waveform.format = self.dirty_waveform.Format(chunk.chff)
        self.dirty_waveform.freq = chunk.chfr
