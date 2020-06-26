from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.filter import BaseFilter


class Filter(BaseFilter, Module):

    flags = 0x000451

    behaviors = {B.receives_audio, B.sends_audio}
