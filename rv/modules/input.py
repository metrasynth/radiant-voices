from enum import Enum

from rv.controller import Controller
from rv.modules import Module


class Input(Module):

    name = mtype = 'Input'
    mgroup = 'Synth'

    class Channels(Enum):
        mono = 0
        stereo = 1

    volume = Controller((0, 1024), 256)
    channels = Controller(Channels, Channels.mono)
