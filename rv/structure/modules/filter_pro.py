from enum import IntEnum

from rv.structure.controller import Controller
from rv.structure.module import GenericModule


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

    _12_DB = 0
    _24_DB = 1
    _36_DB = 2
    _48_DB = 3


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


class FilterProModule(GenericModule):

    class controller_types:
        volume = Controller(0x01, (0, 32768))
        type = Controller(0x02, Type)
        freq_hz = Controller(0x03, (0, 22000))
        freq_finetune = Controller(0x04, (0, 1000))
        freq_scale = Controller(0x05, (0, 200))
        exponential_freq = Controller(0x06, bool)
        q = Controller(0x07, (0, 32768))
        gain = Controller(0x08, (-16384, 16384))
        roll_off = Controller(0x09, RollOff)
        response = Controller(0x0a, (0, 1000))
        mode = Controller(0x0b, Mode)
        mix = Controller(0x0c, (0, 32768))
        lfo_freq = Controller(0x0d, (0, 1024))
        lfo_amp = Controller(0x0e, (0, 32768))
        lfo_waveform = Controller(0x0f, LfoWaveform)
        set_lfo_phase = Controller(0x10, (0, 256))  # used to reset module
        lfo_freq_unit = Controller(0x11, LfoFreqUnit)
