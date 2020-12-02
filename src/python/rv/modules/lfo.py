from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.lfo import BaseLfo


class Lfo(BaseLfo, Module):

    behaviors = {B.sends_audio}
