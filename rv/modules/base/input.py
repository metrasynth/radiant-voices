# -- DO NOT EDIT THIS FILE DIRECTLY --
"""
Base class for Input

This file was auto-generated by rvoxgen.
"""
from enum import Enum


class BaseInput:
    name = "Input"
    mtype = "Input"
    mgroup = "Synth"

    class Channels(Enum):
        mono = 0
        stereo = 1
