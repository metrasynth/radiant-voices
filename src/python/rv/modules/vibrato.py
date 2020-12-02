from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.vibrato import BaseVibrato


class Vibrato(BaseVibrato, Module):

    behaviors = {B.receives_audio, B.sends_audio}
