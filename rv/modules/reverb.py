from enum import Enum

from rv.controller import Controller
from rv.modules import Behavior as B, Module


class Reverb(Module):

    name = mtype = 'Reverb'
    mgroup = 'Effect'

    behaviors = {B.receives_audio, B.sends_audio}

    class Mode(Enum):
        hq = 0
        hq_mono = 1
        lq = 2
        lq_mono = 3

    dry = Controller((0, 256), 256)
    wet = Controller((0, 256), 64)
    feedback = Controller((0, 256), 256)
    damp = Controller((0, 256), 128)
    stereo_width = Controller((0, 256), 256)
    freeze = Controller(bool, False)
    mode = Controller(Mode, Mode.hq)
    all_pass_filter = Controller(bool, True)
    room_size = Controller((0, 128), 16)
