from enum import IntEnum

from rv.controller import Controller
from rv.module import Module


class Channels(IntEnum):

    MONO = 0
    STEREO = 1


class InputModule(Module):

    name = type = 'Input'

    volume = Controller((0, 1024), 256)
    channels = Controller(Channels, Channels.MONO)
