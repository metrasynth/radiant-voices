from enum import Enum

from rv.controller import Controller
from rv.modules import Behavior as B, Module


class FilterPro(Module):

    name = mtype = 'Filter Pro'
    mgroup = 'Effect'

    behaviors = {B.receives_audio, B.sends_audio}

    class Type(Enum):
        lp = 0
        hp = 1
        bp_const_skirt_gain = 2
        bp_const_peak_gain = 3
        notch = 4
        all_pass = 5
        peaking = 6
        low_shelf = 7
        high_shelf = 8

    class RollOff(Enum):
        db_12 = 0
        db_24 = 1
        db_36 = 2
        db_48 = 3

    class Mode(Enum):
        stereo = 0
        mono = 1

    class LfoWaveform(Enum):
        sin = 0
        saw = 1
        saw2 = 2
        square = 3
        random = 4

    class LfoFreqUnit(Enum):
        hz_0_02 = 0  # hz * 0.02
        ms = 1
        hz = 2
        tick = 3
        line = 4
        line_2 = 5  # line / 2
        line_3 = 6  # line / 3

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
