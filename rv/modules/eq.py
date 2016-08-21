from enum import IntEnum

from rv.controller import Controller
from rv.modules import Module


class Eq(Module):

    type = name = 'EQ'
    mgroup = 'Effect'

    class Channels(IntEnum):
        STEREO = 0
        MONO = 1

    low = Controller((0, 512), 256)
    middle = Controller((0, 512), 256)
    high = Controller((0, 512), 256)
    channels = Controller(Channels, Channels.STEREO)
