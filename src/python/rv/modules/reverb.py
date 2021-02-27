from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.reverb import BaseReverb


class Reverb(BaseReverb, Module):

    behaviors = {B.receives_audio, B.sends_audio}
