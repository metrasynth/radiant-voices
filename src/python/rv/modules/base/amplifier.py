# -- DO NOT EDIT THIS FILE DIRECTLY --
"""
Base class for Amplifier
This file was auto-generated by genrv.
"""
from rv.controller import Controller


class BaseAmplifier:
    name = "Amplifier"
    mtype = "Amplifier"
    mgroup = "Effect"
    flags = 0x51
    volume = Controller((0, 1024), 256)
    balance = Controller((-128, 128), 0)
    dc_offset = Controller((-128, 128), 0)
    inverse = Controller(bool, False)
    stereo_width = Controller((0, 256), 128)
    absolute = Controller(bool, False)
    fine_volume = Controller((0, 32768), 32768)
    gain = Controller((0, 5000), 1)
    bipolar_dc_offset = Controller((-16384, 16384), 0)
