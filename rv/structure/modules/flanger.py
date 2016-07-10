from enum import IntEnum

from rv.structure.controller import Controller
from rv.structure.module import GenericModule


class LfoWaveform(IntEnum):

    HSIN = 0
    SIN = 1


class LfoFreqUnit(IntEnum):

    HZ_0_05 = 0     # Hz * 0.05
    MS = 1
    HZ = 2
    TICK = 3
    LINE = 4
    LINE_2 = 5      # line / 2
    LINE_3 = 6      # line / 3


class FlangerModule(GenericModule):

    class controller_types:
        dry = Controller(0x01, (0, 256))
        wet = Controller(0x02, (0, 256))
        feedback = Controller(0x03, (0, 256))
        delay = Controller(0x04, (0, 1000))
        response = Controller(0x05, (0, 256))
        lfo_freq = Controller(0x06, (0, 512))
        lfo_amp = Controller(0x07, (0, 256))
        lfo_waveform = Controller(0x08, LfoWaveform)
        set_lfo_phase = Controller(0x09, (0, 256))  # used to reset module
        lfo_freq_unit = Controller(0x0a, LfoFreqUnit)
