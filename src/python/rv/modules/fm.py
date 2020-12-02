from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.fm import BaseFm


class Fm(BaseFm, Module):

    behaviors = {B.receives_notes, B.sends_audio}
