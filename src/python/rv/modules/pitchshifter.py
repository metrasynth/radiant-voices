from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.pitchshifter import BasePitchShifter


class PitchShifter(BasePitchShifter, Module):

    behaviors = {B.receives_audio, B.sends_audio}
