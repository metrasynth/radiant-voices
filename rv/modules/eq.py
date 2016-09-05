from enum import Enum

from rv.controller import Controller
from rv.modules import Module


class Eq(Module):

    name = mtype = 'EQ'
    mgroup = 'Effect'

    class Channels(Enum):
        stereo = 0
        mono = 1

    low = Controller((0, 512), 256)
    middle = Controller((0, 512), 256)
    high = Controller((0, 512), 256)
    channels = Controller(Channels, Channels.stereo)
