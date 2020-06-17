# -- DO NOT EDIT THIS FILE DIRECTLY --
"""
Base class for Loop

This file was auto-generated by rvoxgen.
"""
from enum import Enum


class BaseLoop:
    name = "Loop"
    mtype = "Loop"
    mgroup = "Effect"

    class Channels(Enum):
        mono = 0
        stereo = 1

    class Mode(Enum):
        normal = 0
        ping_pong = 1
