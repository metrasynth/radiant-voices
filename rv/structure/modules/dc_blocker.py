from enum import IntEnum

from rv.structure.controller import Controller
from rv.structure.module import GenericModule


class Channels(IntEnum):

    STEREO = 0
    MONO = 1


class DcBlockerModule(GenericModule):

    class controller_types:
        channels = Controller(0x01, Channels)
