from enum import IntEnum

from rv.structure.controller import Controller
from rv.structure.module import GenericModule


class Channels(IntEnum):

    MONO = 0
    STEREO = 1


class LoopModule(GenericModule):

    class controller_types:
        volume = Controller(0x01, (0, 256))
        delay = Controller(0x02, (0, 256))      # line / 128
        channels = Controller(0x03, Channels)
        repeats = Controller(0x04, (0, 64))
