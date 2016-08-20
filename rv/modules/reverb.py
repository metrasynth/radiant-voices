from enum import IntEnum

from rv.controller import Controller
from rv.module import Module


class Mode(IntEnum):

    HQ = 0
    HQ_MONO = 1
    LQ = 2
    LQ_MONO = 3


class ReverbModule(Module):

    name = mtype = 'Reverb'

    dry = Controller((0, 256), 256)
    wet = Controller((0, 256), 64)
    feedback = Controller((0, 256), 256)
    damp = Controller((0, 256), 128)
    stereo_width = Controller((0, 256), 256)
    freeze = Controller(bool, False)
    mode = Controller(Mode, mode.HQ)
    all_pass_filter = Controller(bool, True)
    room_size = Controller((0, 128), 16)
