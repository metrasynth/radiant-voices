from enum import IntEnum

from rv.controller import Controller
from rv.modules import Module
from rv.modules import register


class Channels(IntEnum):

    MONO = 0
    STEREO = 1


@register
class LoopModule(Module):

    name = mtype = 'Loop'

    volume = Controller((0, 256), 256)
    delay = Controller((0, 256), 256)  # line / 128
    channels = Controller(Channels, Channels.STEREO)
    repeats = Controller((0, 64), 0)
