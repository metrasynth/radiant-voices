from rv.controller import Controller
from rv.modules import Module


class MetaModule(Module):

    name = mtype = 'MetaModule'
    mgroup = 'Misc'

    # TODO: CHNK, CHNM, CHDT, CHFF, CHFR

    volume = Controller((0, 1024), 256)
    input_module = Controller((1, 256), 1)
    play_patterns = Controller(bool, False)
    bpm = Controller((1, 800), 125)
    tpl = Controller((1, 31), 6)
    # TODO: user defined controllers
