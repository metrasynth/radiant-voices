from enum import Enum

from rv.controller import Controller
from rv.modules import Behavior as B, Module


class Filter(Module):

    name = mtype = 'Filter'
    mgroup = 'Effect'

    behaviors = {B.receives_audio, B.sends_audio}

    class Type(Enum):
        lp = 0
        hp = 1
        bp = 2
        notch = 3

    class Mode(Enum):
        hq = 0
        hq_mono = 1
        lq = 2
        lq_mono = 3

    class RollOff(Enum):
        db_12 = 0
        db_24 = 1
        db_36 = 2
        db_48 = 3

    class LfoFreqUnit(Enum):
        hz_0_02 = 0  # hz * 0.02
        ms = 1
        hz = 2
        tick = 3
        line = 4
        line_2 = 5  # line / 2
        line_3 = 6  # line / 3

    class LfoWaveform(Enum):
        sin = 0
        saw = 1
        saw2 = 2
        square = 3
        random = 4

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
