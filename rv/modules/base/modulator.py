# -- DO NOT EDIT THIS FILE DIRECTLY --
"""
Base class for Modulator
This file was auto-generated by rvoxgen.
"""
from enum import Enum

from rv.controller import Controller


class BaseModulator:
    name = "Modulator"
    mtype = "Modulator"
    mgroup = "Effect"

    class ModulationType(Enum):
        amplitude = 0
        phase = 1
        phase_abs = 2

    class Channels(Enum):
        stereo = 0
        mono = 1

    volume = Controller((0, 512), 256)
    modulation_type = Controller(ModulationType, ModulationType.amplitude)
    channels = Controller(Channels, Channels.stereo)
