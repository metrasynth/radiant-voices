from enum import IntEnum

from rv.structure.controller import Controller
from rv.structure.module import GenericModule


class Channels(IntEnum):

    STEREO = 0
    MONO = 1


class EqModule(GenericModule):

    class controller_types:
        low = Controller(0x01, (0, 512))
        middle = Controller(0x02, (0, 512))
        high = Controller(0x03, (0, 512))
        channels = Controller(0x04, Channels)
