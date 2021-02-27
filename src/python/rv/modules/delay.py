from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.delay import BaseDelay


class Delay(BaseDelay, Module):

    behaviors = {B.receives_audio, B.sends_audio}
