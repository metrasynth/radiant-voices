from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.pitchdetector import BasePitchDetector


class PitchDetector(BasePitchDetector, Module):
    behaviors = {
        B.receives_audio,
        B.sends_notes,
    }
