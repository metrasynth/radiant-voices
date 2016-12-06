from enum import Enum

from rv.chunks import DirtyWaveformChunk
from rv.controller import Controller
from rv.modules import Behavior as B, Module
from rv.option import Option


class AnalogGenerator(Module):

    name = mtype = 'Analog generator'
    mgroup = 'Synth'
    chnk = 0x10
    options_chnm = 0x01

    behaviors = {B.receives_notes, B.sends_audio}

    class Mode(Enum):
        hq = 0
        hq_mono = 1
        lq = 2
        lq_mono = 3

    class Waveform(Enum):
        triangle = 0
        saw = 1
        square = 2
        noise = 3
        drawn = 4
        sin = 5
        hsin = 6
        asin = 7
        drawn_with_spline_interpolation = 8

    class Filter(Enum):
        off = 0
        lp_12db = 1
        hp_12db = 2
        bp_12db = 3
        br_12db = 4
        lp_24db = 5
        hp_24db = 6
        bp_24db = 7
        br_24db = 8

    class FilterEnvelope(Enum):
        off = 0
        sustain_off = 1
        sustain_on = 2

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

    volume_envelope_scaling_per_key = Option(False)
    filter_envelope_scaling_per_key = Option(False)
    volume_scaling_per_key = Option(False)
    filter_freq_scaling_per_key = Option(False)
    velocity_dependent_filter_frequency = Option(False)
    frequency_div_2 = Option(False)
    unsmooth_frequency_change = Option(False)
    filter_freq_scaling_per_key_reverse = Option(False)
    retain_phase = Option(False)
    random_phase = Option(False)
    filter_freq_eq_note_freq = Option(False)
    velocity_dependent_filter_resonance = Option(False)

    def __init__(self, **kwargs):
        samples = kwargs.pop('samples', None)
        super(AnalogGenerator, self).__init__(**kwargs)
        self.dirty_waveform = self.DirtyWaveform()
        if samples is not None:
            self.dirty_waveform.samples = samples

    def specialized_iff_chunks(self):
        for chunk in self.dirty_waveform.chunks():
            yield chunk
        for chunk in super(AnalogGenerator, self).specialized_iff_chunks():
            yield chunk

    def load_chunk(self, chunk):
        if chunk.chnm == self.options_chnm:
            self.load_options(chunk)
        elif chunk.chnm == 0:
            self.load_dirty_waveform(chunk)

    def load_dirty_waveform(self, chunk):
        self.dirty_waveform.samples = chunk.chdt
        self.dirty_waveform.format = self.dirty_waveform.Format(chunk.chff)
        self.dirty_waveform.freq = chunk.chfr
