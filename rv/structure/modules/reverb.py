from enum import IntEnum

from rv.structure.controller import Controller
from rv.structure.module import GenericModule


class Mode(IntEnum):

    HQ = 0
    HQ_MONO = 1
    LQ = 2
    LQ_MONO = 3


class ReverbModule(GenericModule):

    class controller_types:
        dry = Controller(0x01, (0, 256))
        wet = Controller(0x02, (0, 256))
        feedback = Controller(0x03, (0, 256))
        damp = Controller(0x04, (0, 256))
        stereo_width = Controller(0x05, (0, 256))
        freeze = Controller(0x06, bool)
        mode = Controller(0x07, Mode)
        all_pass_filter = Controller(0x08, bool)
        room_size = Controller(0x09, (0, 128))
