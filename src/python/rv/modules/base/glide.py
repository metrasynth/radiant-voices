# -- DO NOT EDIT THIS FILE DIRECTLY --
"""
Base class for Glide
This file was auto-generated by genrv.
"""

from rv.controller import Controller


class BaseGlide:
    name = "Glide"
    mtype = "Glide"
    mgroup = "Misc"
    flags = default_flags = 0x60049
    response = Controller((0, 1000), 500)
    sample_rate = Controller((1, 32768), 150)
    reset_on_first_note = Controller(bool, False)
    polyphony = Controller(bool, True)
    pitch = Controller((-600, 600), 0)
    pitch_scale = Controller((0, 200), 100)
    reset = Controller(bool, False)
    octave = Controller((-10, 10), 0)
    freq_multiply = Controller((1, 256), 1)
    freq_divide = Controller((1, 256), 1)
