# -- DO NOT EDIT THIS FILE DIRECTLY --
"""
Base class for Kicker
This file was auto-generated by genrv.
"""
from enum import IntEnum

from rv.controller import Controller


class BaseKicker:
    name = "Kicker"
    mtype = "Kicker"
    mgroup = "Synth"
    flags = 0x49

    class Waveform(IntEnum):
        triangle = 0
        square = 1
        sin = 2

    volume = Controller((0, 256), 256)
    waveform = Controller(Waveform, Waveform.sin)
    panning = Controller((-128, 128), 0)
    attack = Controller((0, 512), 0)
    release = Controller((0, 512), 32)
    boost = Controller((0, 1024), 0)
    acceleration = Controller((0, 1024), 256)
    polyphony = Controller((1, 4), 1)
    no_click = Controller(bool, False)
