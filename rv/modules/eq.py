from enum import IntEnum

from rv.controller import Controller
from rv.modules import Module
from rv.modules import register


class Channels(IntEnum):

    STEREO = 0
    MONO = 1


@register
class EqModule(Module):

    type = name = 'EQ'

    low = Controller((0, 512), 256)
    middle = Controller((0, 512), 256)
    high = Controller((0, 512), 256)
    channels = Controller(Channels, Channels.STEREO)
