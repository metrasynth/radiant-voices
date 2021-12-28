# -- DO NOT EDIT THIS FILE DIRECTLY --
"""
Base class for FilterPro
This file was auto-generated by genrv.
"""
from enum import IntEnum

from rv.controller import Controller


class BaseFilterPro:
    name = "FilterPro"
    mtype = "Filter Pro"
    mgroup = "Effect"
    flags = 0x451

    class Type(IntEnum):
        lp = 0
        hp = 1
        bp_const_skirt_gain = 2
        bp_const_peak_gain = 3
        notch = 4
        all_pass = 5
        peaking = 6
        low_shelf = 7
        high_shelf = 8
        lp_6dB = 9
        hp_6dB = 10

    class RollOff(IntEnum):
        _12dB = 0
        _24dB = 1
        _36dB = 2
        _48dB = 3

    class Mode(IntEnum):
        stereo = 0
        mono = 1
        stereo_smoothing = 2
        mono_smoothing = 3

    class LfoWaveform(IntEnum):
        sin = 0
        saw = 1
        saw2 = 2
        square = 3
        random = 4

    class LfoFreqUnit(IntEnum):
        hz_mul_0_02 = 0
        ms = 1
        hz = 2
        tick = 3
        line = 4
        line_div_2 = 5
        line_div_3 = 6

    volume = Controller((0, 32768), 32768)
    type = Controller(Type, Type.lp)
    freq = Controller((0, 22000), 22000)
    freq_finetune = Controller((-1000, 1000), 0)
    freq_scale = Controller((0, 200), 100)
    exponential_freq = Controller(bool, False)
    q = Controller((0, 32768), 16384)
    gain = Controller((-16384, 16384), 0)
    roll_off = Controller(RollOff, RollOff._12dB)
    response = Controller((0, 1000), 250)
    mode = Controller(Mode, Mode.stereo)
    mix = Controller((0, 32768), 32768)
    lfo_freq = Controller((0, 1024), 8)
    lfo_amp = Controller((0, 32768), 0)
    lfo_waveform = Controller(LfoWaveform, LfoWaveform.sin)
    set_lfo_phase = Controller((0, 256), 0)
    lfo_freq_unit = Controller(LfoFreqUnit, LfoFreqUnit.hz_mul_0_02)
