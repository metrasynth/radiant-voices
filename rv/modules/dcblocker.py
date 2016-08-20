from enum import IntEnum

from rv.controller import Controller
from rv.module import Module


class Channels(IntEnum):

    STEREO = 0
    MONO = 1


class DcBlockerModule(Module):

    name = mtype = 'DC Blocker'

    channels = Controller(Channels, Channels.STEREO)
