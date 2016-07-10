from enum import IntEnum

from rv.structure.controller import Controller
from rv.structure.module import GenericModule


class VoiceType(IntEnum):

    SOPRANO = 0
    ALTO = 1
    TENOR = 2
    BASS = 3


class Channels(IntEnum):

    STEREO = 0
    MONO = 1


class VocalFilterModule(GenericModule):

    class controller_types:
        volume = Controller(0x01, (0, 512))
        formant_width_hz = Controller(0x02, (0, 256))
        intensity = Controller(0x03, (0, 256))
        formants = Controller(0x04, (1, 5))
        vowel = Controller(0x05, (0, 256))
        voice_type = Controller(0x06, VoiceType)
        channels = Controller(0x07, Channels)
