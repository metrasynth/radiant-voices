from enum import Enum

from rv.controller import Controller
from rv.modules import Module


class Feedback(Module):

    name = mtype = 'Feedback'
    mgroup = 'Misc'

    class Channels(Enum):
        stereo = 0
        mono = 1

    volume = Controller((0, 10000), 1000)
    channels = Controller(Channels, Channels.stereo)
