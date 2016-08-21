from enum import IntEnum

from rv.controller import Controller
from rv.modules import Module


class WaveShaper(Module):

    name = mtype = 'WaveShaper'
    mgroup = 'Effect'

    class Mode(IntEnum):
        HQ = 0
        HQ_MONO = 1
        LQ = 2
        LQ_MONO = 3

    # TODO: CHNK, CHNM, CHDT, CHFF, CHFR

    input_volume = Controller((0, 512), 256)
    mix = Controller((0, 256), 256)
    output_volume = Controller((0, 512), 256)
    symmetric = Controller(bool, True)
    mode = Controller(Mode, Mode.HQ)
    dc_blocker = Controller(bool, True)
