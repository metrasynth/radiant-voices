# -- DO NOT EDIT THIS FILE DIRECTLY --
"""
Base class for FilterPro

This file was auto-generated by rvoxgen.
"""
from enum import Enum


class BaseFilterPro:
    name = "FilterPro"
    mtype = "Filter Pro"
    mgroup = "Effect"

    class Type(Enum):
        lp = 0
        hp = 1
        bp_const_skirt_gain = 2
        bp_const_peak_gain = 3
        notch = 4
        all_pass = 5
        peaking = 6
        low_shelf = 7
        high_shelf = 8

    class RollOff(Enum):
        db_12 = 0
        db_24 = 1
        db_36 = 2
        db_48 = 3

    class Mode(Enum):
        stereo = 0
        mono = 1

    class LfoWaveform(Enum):
        sin = 0
        saw = 1
        saw2 = 2
        square = 3
        random = 4

    class LfoFreqUnit(Enum):
        hz_0_02 = 0
        ms = 1
        hz = 2
        tick = 3
        line = 4
        line_2 = 5
        line_3 = 6
