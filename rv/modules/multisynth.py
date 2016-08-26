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


"""
CHNK: 00000010
CHFF: 00000000
CHFR: 00000000

CHNM: 0
CHDT: <128 bytes representing velocity curve (x = note in, y = velocity out)

CHNM: 1
CHDT: options, 64 bytes:
        0: use static note C5
        1: ignore notes with zero velocity
        2: velocity/velocity curve active
        3:
        4-63: zero padding

CHNM: 2
CHDT: <257 bytes representing velocity curve (x = velocity in, y = velocity out)
"""
