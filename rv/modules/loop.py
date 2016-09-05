from enum import Enum

from rv.controller import Controller
from rv.modules import Module


class Loop(Module):

    name = mtype = 'Loop'
    mgroup = 'Effect'

    class Channels(Enum):
        mono = 0
        stereo = 1

    volume = Controller((0, 256), 256)
    delay = Controller((0, 256), 256)  # line / 128
    channels = Controller(Channels, Channels.stereo)
    repeats = Controller((0, 64), 0)
