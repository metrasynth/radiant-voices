from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.amplifier import BaseAmplifier


class Amplifier(BaseAmplifier, Module):

    behaviors = {B.receives_audio, B.sends_audio}

    receives_audio = True
    sends_audio = True
