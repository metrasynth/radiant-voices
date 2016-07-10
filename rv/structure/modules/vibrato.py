from enum import IntEnum

from rv.structure.controller import Controller
from rv.structure.module import GenericModule


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


class VibratoModule(GenericModule):

    class controller_types:
        volume = Controller(0x01, (0, 256))
        amplitude = Controller(0x02, (0, 256))
        freq = Controller(0x03, (1, 2048))
        channels = Controller(0x04, Channels)
        set_phase = Controller(0x05, (0, 256))  # used to reset module
        frequency_unit = Controller(0x06, FrequencyUnit)
