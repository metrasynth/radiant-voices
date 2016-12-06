from enum import Enum

from rv.controller import Controller
from rv.modules import Behavior as B, Module


class Modulator(Module):

    name = mtype = 'Modulator'
    mgroup = 'Effect'

    behaviors = {B.receives_audio, B.receives_modulator, B.sends_audio}

    class ModulationType(Enum):
        amplitude = 0
        phase = 1
        phase_abs = 2

    class Channels(Enum):
        stereo = 0
        mono = 1

    volume = Controller((0, 512), 256)
    modulation_type = Controller(ModulationType, ModulationType.amplitude)
    channels = Controller(Channels, Channels.stereo)
