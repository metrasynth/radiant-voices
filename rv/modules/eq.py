from enum import IntEnum

from rv.controller import Controller
from rv.module import Module


class Channels(IntEnum):

    STEREO = 0
    MONO = 1


class EqModule(Module):

    type = name = 'EQ'

    low = Controller((0, 512), 256)
    middle = Controller((0, 512), 256)
    high = Controller((0, 512), 256)
    channels = Controller(Channels, Channels.STEREO)
