# -- DO NOT EDIT THIS FILE DIRECTLY --
"""
Base class for Smooth
This file was auto-generated by genrv.
"""
from enum import IntEnum

from rv.controller import Controller


class BaseSmooth:
    name = "Smooth"
    mtype = "Smooth"
    mgroup = "Effect"
    flags = 0x49

    class Mode(IntEnum):
        linear = 0
        lp_filter = 1

    class Channels(IntEnum):
        stereo = 0
        mono = 1

    rise = Controller((0, 32768), 5000)
    fall = Controller((0, 32768), 5000)
    fall_eq_rise = Controller(bool, False)
    scale = Controller((0, 400), 100)
    mode = Controller(Mode, Mode.linear)
    channels = Controller(Channels, Channels.stereo)
