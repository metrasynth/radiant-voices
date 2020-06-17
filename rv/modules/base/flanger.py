# -- DO NOT EDIT THIS FILE DIRECTLY --
"""
Base class for Flanger

This file was auto-generated by rvoxgen.
"""
from enum import Enum


class BaseFlanger:
    name = "Flanger"
    mtype = "Flanger"
    mgroup = "Effect"

    class LfoWaveform(Enum):
        hsin = 0
        sin = 1

    class LfoFreqUnit(Enum):
        hz_0_05 = 0
        ms = 1
        hz = 2
        tick = 3
        line = 4
        line_2 = 5
        line_3 = 6
