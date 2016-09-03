from enum import IntEnum

from rv.controller import Controller
from rv.modules import Module


class Modulator(Module):

    name = mtype = 'Modulator'
    mgroup = 'Effect'

    class ModulationType(IntEnum):
        AMPLITUDE = 0
        PHASE = 1
        PHASE_ABS = 2

    class Channels(IntEnum):
        STEREO = 0
        MONO = 1

    volume = Controller((0, 512), 256)
    modulation_type = Controller(ModulationType, ModulationType.AMPLITUDE)
    channels = Controller(Channels, Channels.STEREO)


Channels = Modulator.Channels
ModulationType = Modulator.ModulationType
