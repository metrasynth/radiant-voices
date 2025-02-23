from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.smooth import BaseSmooth


class Smooth(BaseSmooth, Module):
    behaviors = {B.receives_audio, B.sends_audio}
