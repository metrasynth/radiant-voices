from enum import IntEnum

from rv.structure.controller import Controller
from rv.structure.module import GenericModule


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


class SpectravoiceModule(GenericModule):

    # TODO: CHNK, CHNM, CHDT, CHFF, CHFR

    class controller_types:
        volume = Controller(0x01, (0, 256))
        panning = Controller(0x02, (-128, 128))
        attack = Controller(0x03, (0, 512))
        release = Controller(0x04, (0, 512))
        polyphony_ch = Controller(0x05, (1, 32))
        mode = Controller(0x06, Mode)
        sustain = Controller(0x07, bool)
        spectrum_resolution = Controller(0x08, (0, 5))
        # Note: These are special controllers used to program the module:
        harmonic = Controller(0x09, (0, 15))
        h_freq_hz = Controller(0x0a, (0, 22050))
        h_volume = Controller(0x0b, (0, 255))
        h_width = Controller(0x0c, (0, 255))
        h_type = Controller(0x0d, HarmonicType)
