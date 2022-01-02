# -- DO NOT EDIT THIS FILE DIRECTLY --
"""
Base class for VocalFilter
This file was auto-generated by genrv.
"""
from enum import IntEnum

from rv.controller import Controller


class BaseVocalFilter:
    name = "VocalFilter"
    mtype = "Vocal filter"
    mgroup = "Effect"
    flags = 0x51

    class VoiceType(IntEnum):
        soprano = 0
        alto = 1
        tenor = 2
        bass = 3

    class Channels(IntEnum):
        stereo = 0
        mono = 1

    class Vowel(IntEnum):
        a = 0
        e = 1
        i = 2
        o = 3
        u = 4

    volume = Controller((0, 512), 256)
    formant_width = Controller((0, 256), 128)
    intensity = Controller((0, 256), 128)
    formants = Controller((1, 5), 5)
    vowel = Controller((0, 256), 0)
    voice_type = Controller(VoiceType, VoiceType.soprano)
    channels = Controller(Channels, Channels.stereo)
    random_frequency = Controller((0, 1024), 0)
    random_seed = Controller((0, 32768), 0)
    vowel1 = Controller(Vowel, Vowel.a)
    vowel2 = Controller(Vowel, Vowel.e)
    vowel3 = Controller(Vowel, Vowel.i)
    vowel4 = Controller(Vowel, Vowel.o)
    vowel5 = Controller(Vowel, Vowel.u)
