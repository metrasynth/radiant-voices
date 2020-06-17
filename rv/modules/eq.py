from enum import Enum

from rv.controller import Controller
from rv.modules import Behavior as B, Module
from rv.modules.base.eq import BaseEq


class Eq(BaseEq, Module):

    flags = 0x000051

    behaviors = {B.receives_audio, B.sends_audio}

    class Channels(Enum):
        stereo = 0
        mono = 1

    low = Controller((0, 512), 256)
    middle = Controller((0, 512), 256)
    high = Controller((0, 512), 256)
    channels = Controller(Channels, Channels.stereo)
