from rv.controller import Controller
from rv.modules import Behavior as B, Module
from rv.modules.base.distortion import BaseDistortion


class Distortion(BaseDistortion, Module):

    flags = 0x000051

    behaviors = {B.receives_audio, B.sends_audio}

    Type = BaseDistortion.Type

    volume = Controller((0, 256), 128)
    type = Controller(Type, Type.lim)
    power = Controller((0, 256), 0)
    bit_depth = Controller((1, 16), 16)
    freq_hz = Controller((0, 44100), 44100)
    noise = Controller((0, 256), 0)
