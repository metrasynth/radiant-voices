from enum import Enum

from rv.controller import Controller
from rv.modules import Module


class DcBlocker(Module):

    name = mtype = 'DC Blocker'
    mgroup = 'Effect'

    class Channels(Enum):
        stereo = 0
        mono = 1

    channels = Controller(Channels, Channels.stereo)
