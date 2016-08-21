from enum import IntEnum

from rv.controller import Controller
from rv.modules import Module


class AnalogGenerator(Module):

    name = mtype = 'Analog generator'
    mgroup = 'Synth'

    class Mode(IntEnum):
        HQ = 0
        HQ_MONO = 1
        LQ = 2
        LQ_MONO = 3

    class Waveform(IntEnum):
        TRIANGLE = 0
        SAW = 1
        SQUARE = 2
        NOISE = 3
        DIRTY = 4
        SIN = 5
        HSIN = 6
        ASIN = 7

    class Filter(IntEnum):
        OFF = 0
        LP_12dB = 1
        HP_12dB = 2
        BP_12dB = 3
        BR_12dB = 4
        LP_24dB = 5
        HP_24dB = 6
        BP_24dB = 7
        BR_24dB = 8

    class FilterEnvelope(IntEnum):
        OFF = 0
        SUSTAIN_OFF = 1
        SUSTAIN_ON = 2

    # TODO: CHNK, CHNM, CHDT, CHFF, CHFR

    volume = Controller((0, 256), 80)
    waveform = Controller(Waveform, Waveform.TRIANGLE)
    panning = Controller((-128, 128), 0)
    attack = Controller((0, 256), 0)
    release = Controller((0, 256), 0)
    sustain = Controller(bool, True)
    exponential_envelope = Controller(bool, True)
    duty_cycle = Controller((0, 1024), 512)
    freq2 = Controller((0, 2000), 1000)
    filter = Controller(Filter, Filter.OFF)
    f_freq_hz = Controller((0, 14000), 14000)
    f_resonance = Controller((0, 1530), 0)
    f_exponential_freq = Controller(bool, True)
    f_attack = Controller((0, 256), 0)
    f_release = Controller((0, 256), 0)
    f_envelope = Controller(FilterEnvelope, FilterEnvelope.OFF)
    polyphony_ch = Controller((1, 32), 16)
    mode = Controller(Mode, Mode.HQ)
    noise = Controller((0, 256), 0)
