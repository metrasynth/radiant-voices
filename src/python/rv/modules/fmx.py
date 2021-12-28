from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.fmx import BaseFmx


class Fmx(BaseFmx, Module):

    behaviors = {B.receives_notes, B.sends_audio}
