from enum import Enum

from rv.controller import Controller
from rv.modules import Module


class Vibrato(Module):

    name = mtype = 'Vibrato'
    mgroup = 'Effect'

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

    volume = Controller((0, 256), 256)
    amplitude = Controller((0, 256), 16)
    freq = Controller((1, 2048), 256)
    channels = Controller(Channels, Channels.stereo)
    set_phase = Controller((0, 256), 0)  # used to reset module
    frequency_unit = Controller(FrequencyUnit, FrequencyUnit.hz_64)
