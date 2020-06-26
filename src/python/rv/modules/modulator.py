from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.modulator import BaseModulator


class Modulator(BaseModulator, Module):

    flags = 0x002051

    behaviors = {B.receives_audio, B.receives_modulator, B.sends_audio}
