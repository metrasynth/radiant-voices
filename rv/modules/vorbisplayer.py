from rv.controller import Controller
from rv.modules import Module


class VorbisPlayer(Module):

    name = mtype = 'Vorbis player'
    mgroup = 'Synth'

    # TODO: CHNK, CHNM, CHDT, CHFF, CHFR

    volume = Controller((0, 512), 256)
    original_speed = Controller(bool, True)
    finetune = Controller((-128, 128), 0)
    transpose = Controller((-128, 128), 0)
    interpolation = Controller(bool, True)
    polyphony_ch = Controller((1, 4), 1)
    repeat = Controller(bool, False)


"""
CHNK: 00000010

CHNM: 0
CHDT: <contents of ogg file>
CHFF: 00000000
CHFR: 00000000
"""
