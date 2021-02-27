from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.adsr import BaseAdsr


class Adsr(BaseAdsr, Module):
    behaviors = {
        B.receives_audio,
        B.receives_notes,
        B.sends_audio,
    }
