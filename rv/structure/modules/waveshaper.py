from enum import IntEnum

from rv.structure.controller import Controller
from rv.structure.module import GenericModule


class Mode(IntEnum):

    HQ = 0
    HQ_MONO = 1
    LQ = 2
    LQ_MONO = 3


class WaveshaperModule(GenericModule):

    # TODO: CHNK, CHNM, CHDT, CHFF, CHFR

    class controller_types:
        input_volume = Controller(0x01, (0, 512))
        mix = Controller(0x02, (0, 256))
        output_volume = Controller(0x03, (0, 512))
        symmetric = Controller(0x04, bool)
        mode = Controller(0x05, Mode)
        dc_blocker = Controller(0x06, bool)
