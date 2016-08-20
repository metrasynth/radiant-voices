from enum import IntEnum

from rv.controller import Controller
from rv.module import Module


class Mode(IntEnum):

    HQ = 0
    HQ_MONO = 1
    LQ = 2
    LQ_MONO = 3


class PitchShifterModule(Module):

    name = mtype = 'Pitch shifter'

    volume = Controller((0, 512), 256)
    pitch = Controller((-600, 600), 0)
    pitch_scale = Controller((0, 200), 100)
    feedback = Controller((0, 256), 0)
    grain_size = Controller((0, 256), 64)
    mode = Controller(Mode, Mode.HQ)
