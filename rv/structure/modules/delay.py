from enum import IntEnum

from rv.structure.controller import Controller
from rv.structure.module import GenericModule


class Channels(IntEnum):

    STEREO = 0
    MONO = 1


class DelayUnits(IntEnum):

    SEC_16384 = 0   # sec/16384
    MS = 1
    HZ = 2
    TICK = 3
    LINE = 4
    LINE_2 = 5      # line/2
    LINE_3 = 6      # line/3


class DelayModule(GenericModule):

    class controller_types:
        dry = Controller(0x01, (0, 512))
        wet = Controller(0x02, (0, 512))
        delay_l = Controller(0x03, (0, 256))
        delay_r = Controller(0x04, (0, 256))
        volume_l = Controller(0x05, (0, 256))
        volume_r = Controller(0x06, (0, 256))
        channels = Controller(0x07, Channels)
        inverse = Controller(0x08, bool)
        delay_units = Controller(0x09, DelayUnits)
