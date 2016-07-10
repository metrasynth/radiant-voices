from enum import IntEnum

from rv.structure.controller import Controller
from rv.structure.module import GenericModule


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

    _12_DB = 0
    _24_DB = 1
    _36_DB = 2
    _48_DB = 3


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


class FilterModule(GenericModule):

    class controller_types:
        volume = Controller(0x01, (0, 256))
        freq = Controller(0x02, (0, 14000))
        resonance = Controller(0x03, (0, 1530))
        type = Controller(0x04, Type)
        response = Controller(0x05, (0, 256))
        mode = Controller(0x06, Mode)
        impulse = Controller(0x07, (0, 14000))
        mix = Controller(0x08, (0, 256))
        lfo_freq = Controller(0x09, (0, 1024))
        lfo_amp = Controller(0x0a, (0, 256))
        set_lfo_phase = Controller(0x0b, (0, 256))  # used to reset module?
        exponential_freq = Controller(0x0c, bool)
        roll_off = Controller(0x0d, RollOff)
        lfo_freq_unit = Controller(0x0e, LfoFreqUnit)
        lfo_waveform = Controller(0x0f, LfoWaveform)
