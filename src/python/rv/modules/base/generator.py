# -- DO NOT EDIT THIS FILE DIRECTLY --
"""
Base class for Generator
This file was auto-generated by genrv.
"""
from enum import Enum

from rv.controller import Controller


class BaseGenerator:
    name = "Generator"
    mtype = "Generator"
    mgroup = "Synth"

    class Waveform(Enum):
        triangle = 0
        saw = 1
        square = 2
        noise = 3
        drawn = 4
        sin = 5
        hsin = 6
        asin = 7
        psin = 8

    class Mode(Enum):
        stereo = 0
        mono = 1

    volume = Controller((0, 256), 128)
    waveform = Controller(Waveform, Waveform.triangle)
    panning = Controller((-128, 128), 0)
    attack = Controller((0, 512), 0)
    release = Controller((0, 512), 0)
    polyphony_ch = Controller((1, 16), 8)
    mode = Controller(Mode, Mode.stereo)
    sustain = Controller(bool, True)
    freq_modulation_by_input = Controller((0, 256), 0)
    duty_cycle = Controller((0, 1022), 511)
