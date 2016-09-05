from enum import Enum

from rv.controller import Controller
from rv.modules import Module


class Generator(Module):

    name = mtype = 'Generator'
    mgroup = 'Synth'

    class Waveform(Enum):
        triangle = 0
        saw = 1
        square = 2
        noise = 3
        dirty = 4
        sin = 5
        hsin = 6
        asin = 7
        psin = 8

    class Mode(Enum):
        stereo = 0
        mono = 1

    # TODO: CHNK, CHNM, CHDT, CHFF, CHFR

    volume = Controller((0, 256), 128)
    waveform = Controller(Waveform, Waveform.triangle)
    panning = Controller((-128, 128), 0)
    attack = Controller((0, 512), 0)
    release = Controller((0, 512), 0)
    polyphony_ch = Controller((1, 16), 8)
    mode = Controller(Mode, Mode.stereo)
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
