# -- DO NOT EDIT THIS FILE DIRECTLY --
"""
Base class for Input
This file was auto-generated by genrv.
"""

from enum import IntEnum

from rv.controller import Controller


class BaseInput:
    name = "Input"
    mtype = "Input"
    mgroup = "Synth"
    flags = default_flags = 0x49

    class Channels(IntEnum):
        mono = 0
        stereo = 1

    volume = Controller((0, 1024), 256)
    channels = Controller(Channels, Channels.mono)
