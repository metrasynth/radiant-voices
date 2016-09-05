from enum import IntEnum

from rv.controller import Controller
from rv.modules import Module


class Feedback(Module):

    name = mtype = 'Feedback'
    mgroup = 'Misc'

    class Channels(IntEnum):
        STEREO = 0
        MONO = 1

    volume = Controller((0, 10000), 1000)
    channels = Controller(Channels, Channels.STEREO)
