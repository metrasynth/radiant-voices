# -- DO NOT EDIT THIS FILE DIRECTLY --
"""
Base class for Kicker
This file was auto-generated by genrv.
"""
from enum import Enum

from rv.controller import Controller


class BaseKicker:
    name = "Kicker"
    mtype = "Kicker"
    mgroup = "Synth"

    class Waveform(Enum):
        triangle = 0
        square = 1
        sin = 2

    volume = Controller((0, 256), 256)
    waveform = Controller(Waveform, Waveform.triangle)
    panning = Controller((-128, 128), 0)
    attack = Controller((0, 512), 0)
    release = Controller((0, 512), 32)
    boost = Controller((0, 1024), 0)
    acceleration = Controller((0, 1024), 256)
    polyphony_ch = Controller((1, 4), 1)
    no_click = Controller(bool, False)
