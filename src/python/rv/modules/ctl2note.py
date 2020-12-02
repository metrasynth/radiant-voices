from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.ctl2note import BaseCtl2Note


class Ctl2Note(BaseCtl2Note, Module):
    behaviors = {
        B.sends_notes,
    }
