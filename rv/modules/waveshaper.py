from enum import Enum

from rv.controller import Controller
from rv.modules import Module


class WaveShaper(Module):

    name = mtype = 'WaveShaper'
    mgroup = 'Effect'

    class Mode(Enum):
        hq = 0
        hq_mono = 1
        lq = 2
        lq_mono = 3

    # TODO: CHNK, CHNM, CHDT, CHFF, CHFR

    input_volume = Controller((0, 512), 256)
    mix = Controller((0, 256), 256)
    output_volume = Controller((0, 512), 256)
    symmetric = Controller(bool, True)
    mode = Controller(Mode, Mode.hq)
    dc_blocker = Controller(bool, True)


"""
CHNK: 00000010

CHNM: 0
CHDT: <256 shorts representing waveshaper table>
CHFF: 00000000
CHFR: 00000000
"""
