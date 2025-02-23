# -- DO NOT EDIT THIS FILE DIRECTLY --
"""
Base class for DcBlocker
This file was auto-generated by genrv.
"""

from enum import IntEnum

from rv.controller import Controller


class BaseDcBlocker:
    name = "DcBlocker"
    mtype = "DC Blocker"
    mgroup = "Effect"
    flags = default_flags = 0x51

    class Channels(IntEnum):
        stereo = 0
        mono = 1

    channels = Controller(Channels, Channels.stereo)
