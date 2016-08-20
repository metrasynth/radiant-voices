from enum import IntEnum

from rv.controller import Controller
from rv.module import Module


class Type(IntEnum):

    LP = 0
    HP = 1
    BP_CONST_SKIRT_GAIN = 2
    BP_CONST_PEAK_GAIN = 3
    NOTCH = 4
    ALL_PASS = 5
    PEAKING = 6
    LOW_SHELF = 7
    HIGH_SHELF = 8


class RollOff(IntEnum):

    DB_12 = 0
    DB_24 = 1
    DB_36 = 2
    DB_48 = 3


class Mode(IntEnum):

    STEREO = 0
    MONO = 1


class LfoWaveform(IntEnum):

    SIN = 0
    SAW = 1
    SAW2 = 2
    SQUARE = 3
    RANDOM = 4


class LfoFreqUnit(IntEnum):

    HZ_0_02 = 0     # Hz * 0.02
    MS = 1
    HZ = 2
    TICK = 3
    LINE = 4
    LINE_2 = 5      # line / 2
    LINE_3 = 6      # line / 3


class FilterProModule(Module):

    name = mtype = 'Filter Pro'

    volume = Controller((0, 32768), 32768)
    type = Controller(Type, Type.LP)
    freq_hz = Controller((0, 22000), 22000)
    freq_finetune = Controller((-1000, 1000), 0)
    freq_scale = Controller((0, 200), 100)
    exponential_freq = Controller(bool, False)
    q = Controller((0, 32768), 16384)
    gain = Controller((-16384, 16384), 0)
    roll_off = Controller(RollOff, RollOff.DB_12)
    response = Controller((0, 1000), 250)
    mode = Controller(Mode, Mode.STEREO)
    mix = Controller((0, 32768), 32768)
    lfo_freq = Controller((0, 1024), 8)
    lfo_amp = Controller((0, 32768), 0)
    lfo_waveform = Controller(LfoWaveform, LfoWaveform.SIN)
    set_lfo_phase = Controller((0, 256), 0)  # used to reset module
    lfo_freq_unit = Controller(LfoFreqUnit, LfoFreqUnit.HZ_0_02)
