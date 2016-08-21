from enum import IntEnum

from rv.controller import Controller
from rv.modules import Module


class DcBlocker(Module):

    name = mtype = 'DC Blocker'
    mgroup = 'Effect'

    class Channels(IntEnum):
        STEREO = 0
        MONO = 1

    channels = Controller(Channels, Channels.STEREO)
