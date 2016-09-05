from enum import Enum

from rv.controller import Controller
from rv.modules import Module


class SpectraVoice(Module):

    name = mtype = 'SpectraVoice'
    mgroup = 'Synth'

    class Mode(Enum):
        hq = 0
        hq_mono = 1
        lq = 2
        lq_mono = 3
        hq_spline = 4

    class HarmonicType(Enum):
        hsin = 0
        rect = 1
        org1 = 2
        org2 = 3
        org3 = 4
        org4 = 5
        sin = 6
        random = 7
        triangle1 = 8
        triangle2 = 9
        overtones1 = 10
        overtones2 = 11
        overtones3 = 12
        overtones4 = 13

    # TODO: CHNK, CHNM, CHDT, CHFF, CHFR

    volume = Controller((0, 256), 128)
    panning = Controller((-128, 128), 0)
    attack = Controller((0, 512), 10)
    release = Controller((0, 512), 8000)
    polyphony_ch = Controller((1, 32), 8)
    mode = Controller(Mode, Mode.hq_spline)
    sustain = Controller(bool, True)
    spectrum_resolution = Controller((0, 5), 1)
    # Note: These are controllers used to program the module while it's loaded.
    # When scripting, change the harmonic table directly instead.
    harmonic = Controller((0, 15), 0)
    h_freq_hz = Controller((0, 22050), 1098)
    h_volume = Controller((0, 255), 255)
    h_width = Controller((0, 255), 3)
    h_type = Controller(HarmonicType, HarmonicType.hsin)


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
