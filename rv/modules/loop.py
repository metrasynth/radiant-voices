from enum import Enum

from rv.controller import Controller
from rv.modules import Behavior as B, Module


class Loop(Module):

    name = mtype = 'Loop'
    mgroup = 'Effect'

    behaviors = {B.receives_audio, B.sends_audio}

    class Channels(Enum):
        mono = 0
        stereo = 1

    class Mode(Enum):
        normal = 0
        ping_pong = 1

    volume = Controller((0, 256), 256)
    delay = Controller((0, 256), 256)  # line / 128
    channels = Controller(Channels, Channels.stereo)
    repeats = Controller((0, 64), 0)
    mode = Controller(Mode, Mode.normal)
