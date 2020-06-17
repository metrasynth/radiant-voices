from enum import Enum

from rv.controller import Controller
from rv.modules import Behavior as B, Module
from rv.modules.base.filterpro import BaseFilterPro


class FilterPro(BaseFilterPro, Module):

    flags = 0x000451

    behaviors = {B.receives_audio, B.sends_audio}

    Type = BaseFilterPro.Type
    RollOff = BaseFilterPro.RollOff
    Mode = BaseFilterPro.Mode
    LfoWaveform = BaseFilterPro.LfoWaveform
    LfoFreqUnit = BaseFilterPro.LfoFreqUnit

    volume = Controller((0, 32768), 32768)
    type = Controller(Type, Type.lp)
    freq_hz = Controller((0, 22000), 22000)
    freq_finetune = Controller((-1000, 1000), 0)
    freq_scale = Controller((0, 200), 100)
    exponential_freq = Controller(bool, False)
    q = Controller((0, 32768), 16384)
    gain = Controller((-16384, 16384), 0)
    roll_off = Controller(RollOff, RollOff.db_12)
    response = Controller((0, 1000), 250)
    mode = Controller(Mode, Mode.stereo)
    mix = Controller((0, 32768), 32768)
    lfo_freq = Controller((0, 1024), 8)
    lfo_amp = Controller((0, 32768), 0)
    lfo_waveform = Controller(LfoWaveform, LfoWaveform.sin)
    set_lfo_phase = Controller((0, 256), 0)  # used to reset module
    lfo_freq_unit = Controller(LfoFreqUnit, LfoFreqUnit.hz_0_02)
