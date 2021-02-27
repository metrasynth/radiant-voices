from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.glide import BaseGlide


class Glide(BaseGlide, Module):

    behaviors = {B.receives_notes, B.sends_notes}
