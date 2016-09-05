from enum import IntEnum

from rv.controller import Controller
from rv.modules import Module


class SpectraVoice(Module):

    name = mtype = 'SpectraVoice'
    mgroup = 'Synth'

    class Mode(IntEnum):
        HQ = 0
        HQ_MONO = 1
        LQ = 2
        LQ_MONO = 3
        HQ_SPLINE = 4

    class HarmonicType(IntEnum):
        HSIN = 0
        RECT = 1
        ORG1 = 2
        ORG2 = 3
        ORG3 = 4
        ORG4 = 5
        SIN = 6
        RANDOM = 7
        TRIANGLE1 = 8
        TRIANGLE2 = 9
        OVERTONES1 = 10
        OVERTONES2 = 11
        OVERTONES3 = 12
        OVERTONES4 = 13

    # TODO: CHNK, CHNM, CHDT, CHFF, CHFR

    volume = Controller((0, 256), 128)
    panning = Controller((-128, 128), 0)
    attack = Controller((0, 512), 10)
    release = Controller((0, 512), 8000)
    polyphony_ch = Controller((1, 32), 8)
    mode = Controller(Mode, Mode.HQ_SPLINE)
    sustain = Controller(bool, True)
    spectrum_resolution = Controller((0, 5), 1)
    # Note: These are controllers used to program the module while it's loaded.
    # When scripting, change the harmonic table directly instead.
    harmonic = Controller((0, 15), 0)
    h_freq_hz = Controller((0, 22050), 1098)
    h_volume = Controller((0, 255), 255)
    h_width = Controller((0, 255), 3)
    h_type = Controller(HarmonicType, HarmonicType.HSIN)


"""
CHNK: 00000010
CHFF: 00000000
CHFR: 00000000

CHNM: 0
CHDT: <16 shorts representing h_freq_hz value for each harmonic>

CHNM: 1
CHDT: <16 bytes representing h_volume value for each harmonic>

CHNM: 2
CHDT: <16 bytes representing h_width value for each harmonic>

CHNM: 3
CHDT: <16 bytes representing h_type value for each harmonic>
"""
