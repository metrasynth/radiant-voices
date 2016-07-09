from enum import IntEnum

from rv.structure.controller import Controller, Range
from rv.structure.module import GenericModule


class Waveform(IntEnum):

    TRIANGLE = 0
    SAW = 1
    SQUARE = 2
    NOISE = 3
    DIRTY = 4
    SIN = 5
    HSIN = 6
    ASIN = 7


class Filter(IntEnum):

    OFF = 0
    LP_12dB = 1
    HP_12dB = 2
    BP_12dB = 3
    BR_12dB = 4
    LP_24dB = 5
    HP_24dB = 6
    BP_24dB = 7
    BR_24dB = 8


class FilterEnvelope(IntEnum):

    OFF = 0
    SUSTAIN_OFF = 1
    SUSTAIN_ON = 2


class Mode(IntEnum):

    HQ = 0
    HQ_MONO = 1
    LQ = 2
    LQ_MONO =3


class AnalogGeneratorModule(GenericModule):

    # TODO: CHNK, CHNM, CHDT, CHFF, CHFR

    class controllers(object):
        volume = Controller(0x01, Range(0, 256))
        waveform = Controller(0x02, Waveform)
        panning = Controller(0x03, Range(-128, 128))
        attack = Controller(0x04, Range(0, 256))
        release = Controller(0x05, Range(0, 256))
        sustain = Controller(0x06, bool)
        exponential_envelope = Controller(0x07, bool)
        duty_cycle = Controller(0x08, Range(0, 1024))
        freq2 = Controller(0x09, Range(0, 2000))
        filter = Controller(0x0a, Filter)
        f_freq_hz = Controller(0x0b, Range(0, 14000))
        f_resonance = Controller(0x0c, Range(0, 1530))
        f_exponential_freq = Controller(0x0d, bool)
        f_attack = Controller(0x0e, Range(0, 256))
        f_release = Controller(0x0f, Range(0, 256))
        f_envelope = Controller(0x10, FilterEnvelope)
        polyphony_ch = Controller(0x11, Range(1, 32))
        mode = Controller(0x12, Mode)
        noise = Controller(0x13, Range(0, 256))
