from rv.controller import Controller
from rv.modules import Module


class MultiCtl(Module):

    name = mtype = 'MultiCtl'
    mgroup = 'Misc'

    # TODO: CHNK, CHNM, CHDT, CHFF, CHFR

    value = Controller((0, 32768), 0)
    gain = Controller((0, 1024), 256)
    quantization = Controller((0, 32768), 32768)
