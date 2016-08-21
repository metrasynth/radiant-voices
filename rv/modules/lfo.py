from enum import IntEnum

from rv.controller import Controller
from rv.modules import Module
from rv.modules import register


class Type(IntEnum):

    AMPLITUDE = 0
    PANNING = 1


class Waveform(IntEnum):

    SIN = 0
    SQUARE = 1
    SIN2 = 2
    SAW = 3
    SAW2 = 4


class Channels(IntEnum):

    STEREO = 0
    MONO = 1


class FrequencyUnit(IntEnum):

    HZ_64 = 0       # Hz / 64
    MS = 1
    HZ = 2
    TICK = 3
    LINE = 4
    LINE_2 = 5      # line / 2
    LINE_3 = 6      # line / 3


@register
class LfoModule(Module):

    name = mtype = 'LFO'

    volume = Controller((0, 512), 256)
    type = Controller(Type, Type.AMPLITUDE)
    amplitude = Controller((0, 256), 256)
    freq = Controller((0, 2048), 256)
    waveform = Controller(Waveform, Waveform.SIN)
    set_phase = Controller((0, 256), 0)  # used to reset module
    channels = Controller(Channels, Channels.STEREO)
    frequency_unit = Controller(FrequencyUnit, FrequencyUnit.HZ_64)
    duty_cycle = Controller((0, 256), 128)
