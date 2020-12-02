from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.eq import BaseEq


class Eq(BaseEq, Module):

    behaviors = {B.receives_audio, B.sends_audio}
