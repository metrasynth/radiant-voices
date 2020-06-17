from enum import Enum

from rv.controller import Controller
from rv.modules import Behavior as B, Module
from rv.modules.base.vocalfilter import BaseVocalFilter


class VocalFilter(BaseVocalFilter, Module):

    flags = 0x000051

    behaviors = {B.receives_audio, B.sends_audio}

    VoiceType = BaseVocalFilter.VoiceType
    Channels = BaseVocalFilter.Channels

    volume = Controller((0, 512), 256)
    formant_width_hz = Controller((0, 256), 128)
    intensity = Controller((0, 256), 128)
    formants = Controller((1, 5), 5)
    vowel = Controller((0, 256), 0)
    voice_type = Controller(VoiceType, VoiceType.soprano)
    channels = Controller(Channels, Channels.stereo)
