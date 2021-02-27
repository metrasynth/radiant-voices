from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.loop import BaseLoop


class Loop(BaseLoop, Module):

    behaviors = {B.receives_audio, B.sends_audio}
