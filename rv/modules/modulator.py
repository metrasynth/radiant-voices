from rv.controller import Controller
from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.modulator import BaseModulator


class Modulator(BaseModulator, Module):

    flags = 0x002051

    behaviors = {B.receives_audio, B.receives_modulator, B.sends_audio}

    ModulationType = BaseModulator.ModulationType
    Channels = BaseModulator.Channels

    volume = Controller((0, 512), 256)
    modulation_type = Controller(ModulationType, ModulationType.amplitude)
    channels = Controller(Channels, Channels.stereo)
