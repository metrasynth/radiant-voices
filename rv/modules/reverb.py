from enum import IntEnum

from rv.controller import Controller
from rv.modules import Module


class Reverb(Module):

    name = mtype = 'Reverb'
    mgroup = 'Effect'

    class Mode(IntEnum):
        HQ = 0
        HQ_MONO = 1
        LQ = 2
        LQ_MONO = 3

    dry = Controller((0, 256), 256)
    wet = Controller((0, 256), 64)
    feedback = Controller((0, 256), 256)
    damp = Controller((0, 256), 128)
    stereo_width = Controller((0, 256), 256)
    freeze = Controller(bool, False)
    mode = Controller(Mode, Mode.HQ)
    all_pass_filter = Controller(bool, True)
    room_size = Controller((0, 128), 16)


Mode = Reverb.Mode
