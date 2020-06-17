from rv.controller import Controller
from rv.modules import Behavior as B, Module
from rv.modules.base.flanger import BaseFlanger


class Flanger(BaseFlanger, Module):

    flags = 0x000451

    behaviors = {B.receives_audio, B.sends_audio}

    LfoWaveform = BaseFlanger.LfoWaveform
    LfoFreqUnit = BaseFlanger.LfoFreqUnit

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
