from enum import Enum

from rv.controller import Controller
from rv.modules import Behavior as B, Module
from rv.modules.base.pitchshifter import BasePitchShifter


class PitchShifter(BasePitchShifter, Module):

    flags = 0x000051

    behaviors = {B.receives_audio, B.sends_audio}

    Mode = BasePitchShifter.Mode

    volume = Controller((0, 512), 256)
    pitch = Controller((-600, 600), 0)
    pitch_scale = Controller((0, 200), 100)
    feedback = Controller((0, 256), 0)
    grain_size = Controller((0, 256), 64)
    mode = Controller(Mode, Mode.hq)
