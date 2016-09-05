from enum import Enum

from rv.controller import Controller
from rv.modules import Module


class AnalogGenerator(Module):

    name = mtype = 'Analog generator'
    mgroup = 'Synth'

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
        dirty = 4
        sin = 5
        hsin = 6
        asin = 7

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

    # TODO: CHNK, CHNM, CHDT, CHFF, CHFR

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


"""
CHNK: 00000010

CHNM: 0
CHDT: <32 signed bytes, representing dirty waveform>
        default: 009CA6005A89EC2D 02EC6FE9029E3C20
                 643200CE41623220 A688645A3B150036
CHFF: 0 (8-bit sample)
CHFR: 44100 (AC44)

CHNM: 1
CHDT: options (64 bytes)
        0: volume_envelope_scaling_per_key
        1: filter_envelope_scaling_per_key
        2: volume_scaling_per_key
        3: filter_freq_scaling_per_key
        4: velocity_dependent_filter_freq_scaling
        5: frequency_div_2
        6: unsmooth_frequency_change
        7: filter_freq_scaling_per_key_reverse
        8-63: zero padding
"""
