from enum import IntEnum

from rv.structure.controller import Controller
from rv.structure.module import GenericModule


class Type(IntEnum):

    AMPLITUDE = 0
    PANNING = 1


class Waveform(IntEnum):

    SIN = 0
    SQUARE = 1
    SIN2 = 2
    SAW = 3
    SAW2 = 4


class Channels(IntEnum):

    STEREO = 0
    MONO = 1


class FrequencyUnit(IntEnum):

    HZ_64 = 0       # Hz / 64
    MS = 1
    HZ = 2
    TICK = 3
    LINE = 4
    LINE_2 = 5      # line / 2
    LINE_3 = 6      # line / 3


class LfoModule(GenericModule):

    class controller_types:
        volume = Controller(0x01, (0, 512))
        type = Controller(0x02, Type)
        amplitude = Controller(0x03, (0, 256))
        freq = Controller(0x04, (0, 2048))
        waveform = Controller(0x05, Waveform)
        set_phase = Controller(0x06, (0, 256))  # used to reset module
        channels = Controller(0x07, Channels)
        frequency_unit = Controller(0x08, FrequencyUnit)
        duty_cycle = Controller(0x09, (0, 256))
