from enum import IntEnum

from rv.controller import Controller
from rv.modules import Module
from rv.modules import register


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


@register
class FlangerModule(Module):

    name = mtype = 'Flanger'

    dry = Controller((0, 256), 256)
    wet = Controller((0, 256), 128)
    feedback = Controller((0, 256), 128)
    delay = Controller((0, 1000), 200)
    response = Controller((0, 256), 2)
    lfo_freq = Controller((0, 512), 8)
    lfo_amp = Controller((0, 256), 32)
    lfo_waveform = Controller(LfoWaveform, LfoWaveform.HSIN)
    set_lfo_phase = Controller((0, 256), 0)  # used to reset module
    lfo_freq_unit = Controller(LfoFreqUnit, LfoFreqUnit.HZ_0_05)
