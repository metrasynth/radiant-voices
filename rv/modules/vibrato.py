from enum import IntEnum

from rv.controller import Controller
from rv.modules import Module


class Vibrato(Module):

    name = mtype = 'Vibrato'
    mgroup = 'Effect'

    class Channels(IntEnum):
        STEREO = 0
        MONO = 1

    class FrequencyUnit(IntEnum):
        HZ_64 = 0  # Hz / 64
        MS = 1
        HZ = 2
        TICK = 3
        LINE = 4
        LINE_2 = 5  # line / 2
        LINE_3 = 6  # line / 3

    volume = Controller((0, 256), 256)
    amplitude = Controller((0, 256), 16)
    freq = Controller((1, 2048), 256)
    channels = Controller(Channels, Channels.STEREO)
    set_phase = Controller((0, 256), 0)  # used to reset module
    frequency_unit = Controller(FrequencyUnit, FrequencyUnit.HZ_64)


Channels = Vibrato.Channels
FrequencyUnit = Vibrato.FrequencyUnit
