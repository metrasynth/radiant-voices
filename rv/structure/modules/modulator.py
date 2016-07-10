from enum import IntEnum

from rv.structure.controller import Controller
from rv.structure.module import GenericModule


class ModulationType(IntEnum):

    AMPLITUDE = 0
    PHASE = 1
    PHASE_ABS = 2


class Channels(IntEnum):

    STEREO = 0
    MONO = 1


class ModulatorModule(GenericModule):

    class controller_types:
        volume = Controller(0x01, (0, 512))
        modulation_type = Controller(0x02, ModulationType)
        channels = Controller(0x03, Channels)
