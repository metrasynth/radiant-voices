from enum import IntEnum

from rv.controller import Controller
from rv.modules import Module


class VocalFilter(Module):

    name = mtype = 'Vocal filter'
    mgroup = 'Effect'

    class VoiceType(IntEnum):
        SOPRANO = 0
        ALTO = 1
        TENOR = 2
        BASS = 3

    class Channels(IntEnum):
        STEREO = 0
        MONO = 1

    volume = Controller((0, 512), 256)
    formant_width_hz = Controller((0, 256), 128)
    intensity = Controller((0, 256), 128)
    formants = Controller((1, 5), 5)
    vowel = Controller((0, 256), 0)
    voice_type = Controller(VoiceType, VoiceType.SOPRANO)
    channels = Controller(Channels, Channels.STEREO)


Channels = VocalFilter.Channels
VoiceType = VocalFilter.VoiceType
