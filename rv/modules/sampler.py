from enum import IntEnum

from rv.controller import Controller
from rv.modules import Module


class Sampler(Module):

    name = mtype = 'Sampler'
    mgroup = 'Synth'

    class SampleInterpolation(IntEnum):
        OFF = 0
        LINEAR = 1
        SPLINE = 2

    class EnvelopeInterpolation(IntEnum):
        OFF = 0
        LINEAR = 1

    # TODO: CHNK, CHNM, CHDT, CHFF, CHFR

    volume = Controller((0, 512), 256)
    panning = Controller((-128, 128), 0)
    sample_interpoluation = Controller(SampleInterpolation, SampleInterpolation.SPLINE)
    envelope_interpolation = Controller(EnvelopeInterpolation, EnvelopeInterpolation.LINEAR)
    polyphony_ch = Controller((1, 32), 8)
    rec_threshold = Controller((0, 10000), 4)
