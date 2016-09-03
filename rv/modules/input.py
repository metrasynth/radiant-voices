from enum import IntEnum

from rv.controller import Controller
from rv.modules import Module


class Input(Module):

    name = mtype = 'Input'
    mgroup = 'Synth'

    class Channels(IntEnum):
        MONO = 0
        STEREO = 1

    volume = Controller((0, 1024), 256)
    channels = Controller(Channels, Channels.MONO)


Channels = Input.Channels
