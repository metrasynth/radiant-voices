from enum import IntEnum

from rv.controller import Controller
from rv.module import Module


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


class EchoModule(Module):

    type = name = 'Echo'

    dry = Controller((0, 256), 256)
    wet = Controller((0, 256), 128)
    feedback = Controller((0, 256), 128)
    delay = Controller((0, 256), 256)
    channels = Controller(Channels, Channels.STEREO)
    delay_units = Controller(DelayUnits, DelayUnits.SEC_256)
