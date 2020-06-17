from rv.controller import Controller
from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.filter import BaseFilter


class Filter(BaseFilter, Module):

    flags = 0x000451

    behaviors = {B.receives_audio, B.sends_audio}

    Type = BaseFilter.Type
    Mode = BaseFilter.Mode
    RollOff = BaseFilter.RollOff
    LfoFreqUnit = BaseFilter.LfoFreqUnit
    LfoWaveform = BaseFilter.LfoWaveform

    volume = Controller((0, 256), 256)
    freq = Controller((0, 14000), 14000)
    resonance = Controller((0, 1530), 0)
    type = Controller(Type, Type.lp)
    response = Controller((0, 256), 8)
    mode = Controller(Mode, Mode.hq)
    impulse = Controller((0, 14000), 0)
    mix = Controller((0, 256), 256)
    lfo_freq = Controller((0, 1024), 8)
    lfo_amp = Controller((0, 256), 0)
    set_lfo_phase = Controller((0, 256), 0)  # used to reset module
    exponential_freq = Controller(bool, False)
    roll_off = Controller(RollOff, RollOff.db_12)
    lfo_freq_unit = Controller(LfoFreqUnit, LfoFreqUnit.hz_0_02)
    lfo_waveform = Controller(LfoWaveform, LfoWaveform.sin)
