from enum import IntEnum

from rv.structure.controller import Controller
from rv.structure.module import GenericModule


class Channels(IntEnum):

    MONO = 0
    STEREO = 1


class Mode(IntEnum):

    LQ = 0
    HQ = 1


class Sound2CtlModule(GenericModule):

    # TODO: CHNK, CHNM, CHDT, CHFF, CHFR

    class controller_types:
        sample_rate_hz = Controller(0x01, (1, 32768))
        channels = Controller(0x02, Channels)
        absolute = Controller(0x03, bool)
        gain = Controller(0x04, (0, 1024))
        smooth = Controller(0x05, (0, 256))
        mode = Controller(0x06, Mode)
        out_min = Controller(0x07, (0, 32768))
        out_max = Controller(0x08, (0, 32768))
        out_controller = Controller(0x09, (0, 32))
