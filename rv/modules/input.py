from enum import IntEnum

from rv.controller import Controller
from rv.modules import Module
from rv.modules import register


class Channels(IntEnum):

    MONO = 0
    STEREO = 1


@register
class InputModule(Module):

    name = mtype = 'Input'

    volume = Controller((0, 1024), 256)
    channels = Controller(Channels, Channels.MONO)
