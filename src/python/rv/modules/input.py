from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.input import BaseInput


class Input(BaseInput, Module):

    behaviors = {B.sends_audio}
