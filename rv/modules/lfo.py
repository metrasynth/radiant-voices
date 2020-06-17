from rv.controller import Controller, DependentRange, Range, WarnOnlyRange
from rv.modules import Behavior as B, Module
from rv.modules.base.lfo import BaseLfo


class Lfo(BaseLfo, Module):

    flags = 0x000451

    behaviors = {B.sends_audio}

    Type = BaseLfo.Type
    Waveform = BaseLfo.Waveform
    Channels = BaseLfo.Channels
    FrequencyUnit = BaseLfo.FrequencyUnit

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
