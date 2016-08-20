from enum import IntEnum

from rv.controller import Controller
from rv.module import Module


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


class DelayModule(Module):

    name = mtype = 'Delay'

    class controller_types:
        dry = Controller((0, 512), 256)
        wet = Controller((0, 512), 256)
        delay_l = Controller((0, 256), 128)
        delay_r = Controller((0, 256), 160)
        volume_l = Controller((0, 256), 256)
        volume_r = Controller((0, 256), 256)
        channels = Controller(Channels, Channels.STEREO)
        inverse = Controller(bool, False)
        delay_units = Controller(DelayUnits, DelayUnits.SEC_16384)
