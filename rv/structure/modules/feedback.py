from enum import IntEnum

from rv.structure.controller import Controller
from rv.structure.module import GenericModule


class Channels(IntEnum):

    STEREO = 0
    MONO = 1


class FeedbackModule(GenericModule):

    class controller_types:
        volume = Controller(0x01, (0, 10000))
        channels = Controller(0x02, Channels)
