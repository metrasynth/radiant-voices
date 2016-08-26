from enum import IntEnum

from rv.controller import Controller
from rv.modules import Module


class Generator(Module):

    name = mtype = 'Generator'
    mgroup = 'Synth'

    class Waveform(IntEnum):
        TRIANGLE = 0
        SAW = 1
        SQUARE = 2
        NOISE = 3
        DIRTY = 4
        SIN = 5
        HSIN = 6
        ASIN = 7
        PSIN = 8

    class Mode(IntEnum):
        STEREO = 0
        MONO = 1

    # TODO: CHNK, CHNM, CHDT, CHFF, CHFR

    volume = Controller((0, 256), 128)
    waveform = Controller(Waveform, Waveform.TRIANGLE)
    panning = Controller((-128, 128), 0)
    attack = Controller((0, 512), 0)
    release = Controller((0, 512), 0)
    polyphony_ch = Controller((1, 16), 8)
    mode = Controller(Mode, Mode.STEREO)
    sustain = Controller(bool, True)
    freq_modulation_input = Controller((0, 256), 0)
    duty_cycle = Controller((0, 1022), 511)


"""
CHNK: 00000010

CHNM: 0
CHDT: <32 signed bytes, representing dirty waveform>
        default: 009CA6005A89EC2D 02EC6FE9029E3C20
                 643200CE41623220 A688645A3B150036
CHFF: 0 (8-bit sample)
CHFR: 44100 (AC44)
"""
