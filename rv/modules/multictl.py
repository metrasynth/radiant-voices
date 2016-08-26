from rv.controller import Controller
from rv.modules import Module


class MultiCtl(Module):

    name = mtype = 'MultiCtl'
    mgroup = 'Misc'

    # TODO: CHNK, CHNM, CHDT, CHFF, CHFR

    value = Controller((0, 32768), 0)
    gain = Controller((0, 1024), 256)
    quantization = Controller((0, 32768), 32768)


"""
CHNK: 00000010
CHFF: 00000000
CHFR: 00000000

CHNM: 0
CHDT: <repeated 16 times: 0000000000800000 0000000000000000 0000000000000000 0000000000000000>

CHNM: 1
CHDT: <257 shorts representing value mapping (x = value in, y = value out)>
"""
