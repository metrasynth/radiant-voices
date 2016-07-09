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
    PSIN = 8


class Mode(IntEnum):
    STEREO = 0
    MONO = 1


class GeneratorModule(GenericModule):

    class controller_types(object):
        volume = Controller(0x01, Range(0, 256))
        waveform = Controller(0x02, Waveform)
        panning = Controller(0x03, Range(-128, 128))
        attack = Controller(0x04, Range(0, 512))
        release = Controller(0x05, Range(0, 512))
        polyphony_ch = Controller(0x06, Range(1, 16))
        mode = Controller(0x07, Mode)
        sustain = Controller(0x08, bool)
        freq_modulation_input = Controller(0x09, Range(0, 256))
        duty_cycle = Controller(0x0a, Range(0, 1022))
