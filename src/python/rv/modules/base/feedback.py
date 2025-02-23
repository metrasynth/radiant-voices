# -- DO NOT EDIT THIS FILE DIRECTLY --
"""
Base class for Feedback
This file was auto-generated by genrv.
"""

from enum import IntEnum

from rv.controller import Controller


class BaseFeedback:
    name = "Feedback"
    mtype = "Feedback"
    mgroup = "Misc"
    flags = default_flags = 0x600051

    class Channels(IntEnum):
        stereo = 0
        mono = 1

    volume = Controller((0, 10000), 1000)
    channels = Controller(Channels, Channels.stereo)
