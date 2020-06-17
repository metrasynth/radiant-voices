from rv.chunks import DirtyWaveformChunk
from rv.controller import Controller
from rv.modules import Behavior as B, Module
from rv.modules.base.analoggenerator import BaseAnalogGenerator


class AnalogGenerator(BaseAnalogGenerator, Module):

    chnk = 2
    options_chnm = 1
    flags = 0x000049

    behaviors = {B.receives_notes, B.sends_audio}

    Mode = BaseAnalogGenerator.Mode
    Waveform = BaseAnalogGenerator.Waveform
    Filter = BaseAnalogGenerator.Filter
    FilterEnvelope = BaseAnalogGenerator.FilterEnvelope

    class DirtyWaveform(DirtyWaveformChunk):
        chnm = 0

    volume = Controller((0, 256), 80)
    waveform = Controller(Waveform, Waveform.triangle)
    panning = Controller((-128, 128), 0)
    attack = Controller((0, 256), 0)
    release = Controller((0, 256), 0)
    sustain = Controller(bool, True)
    exponential_envelope = Controller(bool, True)
    duty_cycle = Controller((0, 1024), 512)
    freq2 = Controller((0, 2000), 1000)
    filter = Controller(Filter, Filter.off)
    f_freq_hz = Controller((0, 14000), 14000)
    f_resonance = Controller((0, 1530), 0)
    f_exponential_freq = Controller(bool, True)
    f_attack = Controller((0, 256), 0)
    f_release = Controller((0, 256), 0)
    f_envelope = Controller(FilterEnvelope, FilterEnvelope.off)
    polyphony_ch = Controller((1, 32), 16)
    mode = Controller(Mode, Mode.hq)
    noise = Controller((0, 256), 0)

    def __init__(self, **kwargs):
        samples = kwargs.pop("samples", None)
        super(AnalogGenerator, self).__init__(**kwargs)
        self.dirty_waveform = self.DirtyWaveform()
        if samples is not None:
            self.dirty_waveform.samples = samples

    def specialized_iff_chunks(self):
        yield from self.dirty_waveform.chunks()
        yield from super(AnalogGenerator, self).specialized_iff_chunks()

    def load_chunk(self, chunk):
        if chunk.chnm == self.options_chnm:
            self.load_options(chunk)
        elif chunk.chnm == 0:
            self.load_dirty_waveform(chunk)

    def load_dirty_waveform(self, chunk):
        self.dirty_waveform.samples = chunk.chdt
        self.dirty_waveform.format = self.dirty_waveform.Format(chunk.chff or 1)
        self.dirty_waveform.freq = chunk.chfr
