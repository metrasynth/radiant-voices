from enum import IntEnum

from rv.structure.controller import Controller
from rv.structure.module import GenericModule


class Mode(IntEnum):

    PEAK = 0
    RMS = 1


class CompressorModule(GenericModule):

    class controller_types:
        volume = Controller(0x01, (0, 512))
        threshold = Controller(0x02, (0, 512))
        slope_pct = Controller(0x03, (0, 200))
        attack_ms = Controller(0x04, (0, 500))
        release_ms = Controller(0x05, (1, 1000))
        mode = Controller(0x06, Mode)
        sidechain_input = Controller(0x07, (0, 32))
