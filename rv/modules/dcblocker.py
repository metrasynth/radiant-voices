from enum import Enum

from rv.controller import Controller
from rv.modules import Behavior as B, Module
from rv.modules.base.dcblocker import BaseDcBlocker


class DcBlocker(BaseDcBlocker, Module):

    name = mtype = "DC Blocker"
    flags = 0x000051

    behaviors = {B.receives_audio, B.sends_audio}

    class Channels(Enum):
        stereo = 0
        mono = 1

    channels = Controller(Channels, Channels.stereo)
