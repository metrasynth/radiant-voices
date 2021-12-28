# -- DO NOT EDIT THIS FILE DIRECTLY --
"""
Base class for Fm
This file was auto-generated by genrv.
"""
from enum import IntEnum

from rv.controller import Controller


class BaseFm:
    name = "Fm"
    mtype = "FM"
    mgroup = "Synth"
    flags = 0x49

    class Mode(IntEnum):
        hq = 0
        hq_mono = 1
        lq = 2
        lq_mono = 3

    c_volume = Controller((0, 256), 128)
    m_volume = Controller((0, 256), 48)
    panning = Controller((-128, 128), 0)
    c_freq_ratio = Controller((0, 16), 1)
    m_freq_ratio = Controller((0, 16), 1)
    m_self_modulation = Controller((0, 256), 0)
    c_attack = Controller((0, 512), 32)
    c_decay = Controller((0, 512), 32)
    c_sustain = Controller((0, 256), 128)
    c_release = Controller((0, 512), 64)
    m_attack = Controller((0, 512), 32)
    m_decay = Controller((0, 512), 32)
    m_sustain = Controller((0, 256), 128)
    m_release = Controller((0, 512), 64)
    m_scaling_per_key = Controller((0, 4), 0)
    polyphony = Controller((1, 16), 4)
    mode = Controller(Mode, Mode.hq)
