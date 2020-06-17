from enum import Enum

from rv.controller import Controller, DependentRange, Range, WarnOnlyRange
from rv.modules import Behavior as B, Module
from rv.modules.base.lfo import BaseLfo


class Lfo(BaseLfo, Module):

    name = mtype = "LFO"
    flags = 0x000451

    behaviors = {B.sends_audio}

    class Type(Enum):
        amplitude = 0
        panning = 1

    class Waveform(Enum):
        sin = 0
        square = 1
        sin2 = 2
        saw = 3
        saw2 = 4
        random = 5
        triangle = 6
        random_interpolated = 7

    class Channels(Enum):
        stereo = 0
        mono = 1

    class FrequencyUnit(Enum):
        hz_64 = 0  # hz / 64
        ms = 1
        hz = 2
        tick = 3
        line = 4
        line_2 = 5  # line / 2
        line_3 = 6  # line / 3

    freq_ranges = {
        FrequencyUnit.hz_64: WarnOnlyRange(1, 2048),
        FrequencyUnit.ms: WarnOnlyRange(1, 4000),
        FrequencyUnit.hz: WarnOnlyRange(1, 16384),
        FrequencyUnit.tick: WarnOnlyRange(1, 256),
        FrequencyUnit.line: WarnOnlyRange(1, 256),
        FrequencyUnit.line_2: WarnOnlyRange(1, 256),
        FrequencyUnit.line_3: WarnOnlyRange(1, 256),
    }

    volume = Controller((0, 512), 256)
    type = Controller(Type, Type.amplitude)
    amplitude = Controller((0, 256), 256)
    freq = Controller(
        DependentRange("frequency_unit", freq_ranges, Range(1, 2048)), 256
    )
    waveform = Controller(Waveform, Waveform.sin)
    set_phase = Controller((0, 256), 0)  # used to reset module
    channels = Controller(Channels, Channels.stereo)
    frequency_unit = Controller(FrequencyUnit, FrequencyUnit.hz_64)
    duty_cycle = Controller((0, 256), 128)
    generator = Controller(bool, False)
