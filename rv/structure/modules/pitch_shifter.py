from enum import IntEnum

from rv.structure.controller import Controller
from rv.structure.module import GenericModule


class Mode(IntEnum):

    HQ = 0
    HQ_MONO = 1
    LQ = 2
    LQ_MONO = 3


class PitchShifterModule(GenericModule):

    class controller_types:
        volume = Controller(0x01, (0, 512))
        pitch = Controller(0x02, (-600, 600))
        pitch_scale = Controller(0x03, (0, 200))
        feedback = Controller(0x04, (0, 256))
        grain_size = Controller(0x05, (0, 256))
        mode = Controller(0x06, Mode)
