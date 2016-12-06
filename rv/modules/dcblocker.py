from enum import Enum

from rv.controller import Controller
from rv.modules import Behavior as B, Module


class DcBlocker(Module):

    name = mtype = 'DC Blocker'
    mgroup = 'Effect'

    behaviors = {B.receives_audio, B.sends_audio}

    class Channels(Enum):
        stereo = 0
        mono = 1

    channels = Controller(Channels, Channels.stereo)
