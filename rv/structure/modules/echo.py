from enum import IntEnum

from rv.structure.controller import Controller
from rv.structure.module import GenericModule


class Channels(IntEnum):

    MONO = 0
    STEREO = 1


class DelayUnits(IntEnum):

    SEC_256 = 0     # sec/256
    MS = 1
    HZ = 2
    TICK = 3
    LINE = 4
    LINE_2 = 5      # line/2
    LINE_3 = 6      # line/3


class EchoModule(GenericModule):

    class controller_types:
        dry = Controller(0x01, (0, 256))
        wet = Controller(0x02, (0, 256))
        feedback = Controller(0x03, (0, 256))
        delay = Controller(0x04, (0, 256))
        channels = Controller(0x05, Channels)
        delay_units = Controller(0x06, DelayUnits)
