from enum import IntEnum

from rv.structure.controller import Controller
from rv.structure.module import GenericModule


class SampleInterpolation(IntEnum):

    OFF = 0
    LINEAR = 1
    SPLINE = 2


class EnvelopeInterpolation(IntEnum):

    OFF = 0
    LINEAR = 1


class SamplerModule(GenericModule):

    # TODO: CHNK, CHNM, CHDT, CHFF, CHFR

    class controller_types:
        volume = Controller(0x01, (0, 512))
        panning = Controller(0x02, (-128, 128))
        sample_interpoluation = Controller(0x03, SampleInterpolation)
        envelope_interpolation = Controller(0x04, EnvelopeInterpolation)
        polyphony_ch = Controller(0x05, (1, 32))
        rec_threshold = Controller(0x06, (0, 10000))
