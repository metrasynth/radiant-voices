from enum import Enum

from rv.controller import Controller
from rv.modules import Behavior as B, Module


class Lfo(Module):

    name = mtype = 'LFO'
    mgroup = 'Effect'

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

    volume = Controller((0, 512), 256)
    type = Controller(Type, Type.amplitude)
    amplitude = Controller((0, 256), 256)
    freq = Controller((0, 2048), 256)
    waveform = Controller(Waveform, Waveform.sin)
    set_phase = Controller((0, 256), 0)  # used to reset module
    channels = Controller(Channels, Channels.stereo)
    frequency_unit = Controller(FrequencyUnit, FrequencyUnit.hz_64)
    duty_cycle = Controller((0, 256), 128)
