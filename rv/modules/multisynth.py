from rv.controller import Controller
from rv.modules import Module


class MultiSynth(Module):

    name = mtype = 'MultiSynth'
    mgroup = 'Misc'

    # TODO: CHNK, CHNM, CHDT, CHFF, CHFR

    transpose = Controller((-128, 128), 0)
    random_pitch = Controller((0, 4096), 0)
    velocity = Controller((0, 256), 256)
    finetune = Controller((-256, 256), 0)
    random_phase = Controller((0, 32768), 0)
    random_velocity = Controller((0, 32768), 0)
    phase = Controller((0, 32768), 0)
