# -- DO NOT EDIT THIS FILE DIRECTLY --
"""
Base class for Modulator
This file was auto-generated by genrv.
"""

from enum import IntEnum

from rv.controller import Controller


class BaseModulator:
    name = "Modulator"
    mtype = "Modulator"
    mgroup = "Effect"
    flags = default_flags = 0x2051

    class ModulationType(IntEnum):
        amplitude = 0
        phase = 1
        phase_abs = 2
        add = 3
        sub = 4
        min = 5
        max = 6
        bitwise_and = 7
        bitwise_xor = 8
        min_abs = 9
        max_abs = 10

    class Channels(IntEnum):
        stereo = 0
        mono = 1

    class MaxPhaseModulationDelay(IntEnum):
        sec_0_04 = 0
        sec_0_08 = 1
        sec_0_2 = 2
        sec_0_5 = 3
        sec_1 = 4
        sec_2 = 5
        sec_4 = 6

    volume = Controller((0, 512), 256)
    modulation_type = Controller(ModulationType, ModulationType.amplitude)
    channels = Controller(Channels, Channels.stereo)
    max_phase_modulation_delay = Controller(
        MaxPhaseModulationDelay, MaxPhaseModulationDelay.sec_0_04
    )
