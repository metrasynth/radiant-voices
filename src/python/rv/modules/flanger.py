from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.flanger import BaseFlanger


class Flanger(BaseFlanger, Module):

    behaviors = {B.receives_audio, B.sends_audio}
