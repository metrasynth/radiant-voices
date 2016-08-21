from enum import IntEnum

from rv.controller import Controller
from rv.modules import Module
from rv.modules import register


class ModulationType(IntEnum):

    AMPLITUDE = 0
    PHASE = 1
    PHASE_ABS = 2


class Channels(IntEnum):

    STEREO = 0
    MONO = 1


@register
class ModulatorModule(Module):

    name = mtype = 'Modulator'

    volume = Controller((0, 512), 256)
    modulation_type = Controller(ModulationType, ModulationType.AMPLITUDE)
    channels = Controller(Channels, Channels.STEREO)
