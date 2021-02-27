from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.pitch2ctl import BasePitch2Ctl


class Pitch2Ctl(BasePitch2Ctl, Module):

    behaviors = {B.receives_notes, B.sends_controls}
