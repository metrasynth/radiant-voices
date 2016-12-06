from enum import Enum

from rv.controller import Controller
from rv.modules import Behavior as B, Module


class Flanger(Module):

    name = mtype = 'Flanger'
    mgroup = 'Effect'

    behaviors = {B.receives_audio, B.sends_audio}

    class LfoWaveform(Enum):
        hsin = 0
        sin = 1

    class LfoFreqUnit(Enum):
        hz_0_05 = 0  # hz * 0.05
        ms = 1
        hz = 2
        tick = 3
        line = 4
        line_2 = 5  # line / 2
        line_3 = 6  # line / 3

    dry = Controller((0, 256), 256)
    wet = Controller((0, 256), 128)
    feedback = Controller((0, 256), 128)
    delay = Controller((0, 1000), 200)
    response = Controller((0, 256), 2)
    lfo_freq = Controller((0, 512), 8)
    lfo_amp = Controller((0, 256), 32)
    lfo_waveform = Controller(LfoWaveform, LfoWaveform.hsin)
    set_lfo_phase = Controller((0, 256), 0)  # used to reset module
    lfo_freq_unit = Controller(LfoFreqUnit, LfoFreqUnit.hz_0_05)
