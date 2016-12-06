from enum import Enum

from rv.controller import Controller
from rv.modules import Behavior as B, Module


class Distortion(Module):

    name = mtype = 'Distortion'
    mgroup = 'Effect'

    behaviors = {B.receives_audio, B.sends_audio}

    class Type(Enum):
        lim = 0
        sat = 1

    volume = Controller((0, 256), 128)
    type = Controller(Type, Type.lim)
    power = Controller((0, 256), 0)
    bit_depth = Controller((1, 16), 16)
    freq_hz = Controller((0, 44100), 44100)
    noise = Controller((0, 256), 0)
