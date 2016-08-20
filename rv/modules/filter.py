from enum import IntEnum

from rv.controller import Controller
from rv.module import Module


class Type(IntEnum):

    LP = 0
    HP = 1
    BP = 2
    NOTCH = 3


class Mode(IntEnum):

    HQ = 0
    HQ_MONO = 1
    LQ = 2
    LQ_MONO = 3


class RollOff(IntEnum):

    DB_12 = 0
    DB_24 = 1
    DB_36 = 2
    DB_48 = 3


class LfoFreqUnit(IntEnum):

    HZ_0_02 = 0     # Hz * 0.02
    MS = 1
    HZ = 2
    TICK = 3
    LINE = 4
    LINE_2 = 5      # line / 2
    LINE_3 = 6      # line / 3


class LfoWaveform(IntEnum):

    SIN = 0
    SAW = 1
    SAW2 = 2
    SQUARE = 3
    RANDOM = 4


class FilterModule(Module):

    name = mtype = 'Filter'

    volume = Controller((0, 256), 256)
    freq = Controller((0, 14000), 14000)
    resonance = Controller((0, 1530), 0)
    type = Controller(Type, Type.LP)
    response = Controller((0, 256), 8)
    mode = Controller(Mode, Mode.HQ)
    impulse = Controller((0, 14000), 0)
    mix = Controller((0, 256), 256)
    lfo_freq = Controller((0, 1024), 8)
    lfo_amp = Controller((0, 256), 0)
    set_lfo_phase = Controller((0, 256), 0)  # used to reset module
    exponential_freq = Controller(bool, False)
    roll_off = Controller(RollOff, RollOff.DB_12)
    lfo_freq_unit = Controller(LfoFreqUnit, LfoFreqUnit.HZ_0_02)
    lfo_waveform = Controller(LfoWaveform, LfoWaveform.SIN)
