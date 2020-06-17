from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.kicker import BaseKicker


class Kicker(BaseKicker, Module):

    flags = 0x000049

    behaviors = {B.receives_notes, B.sends_audio}
