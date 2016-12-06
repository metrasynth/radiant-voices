from enum import Enum

from rv.controller import Controller
from rv.modules import Behavior as B, Module


class PitchShifter(Module):

    name = mtype = 'Pitch shifter'
    mgroup = 'Effect'

    behaviors = {B.receives_audio, B.sends_audio}

    class Mode(Enum):
        hq = 0
        hq_mono = 1
        lq = 2
        lq_mono = 3

    volume = Controller((0, 512), 256)
    pitch = Controller((-600, 600), 0)
    pitch_scale = Controller((0, 200), 100)
    feedback = Controller((0, 256), 0)
    grain_size = Controller((0, 256), 64)
    mode = Controller(Mode, Mode.hq)
