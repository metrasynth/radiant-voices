from enum import IntEnum

from rv.controller import Controller
from rv.module import Module


class Type(IntEnum):

    LIM = 0
    SAT = 1


class DistortionModule(Module):

    name = mtype = 'Distortion'

    class controller_types:
        volume = Controller((0, 256), 128)
        type = Controller(Type, Type.LIM)
        power = Controller((0, 256), 0)
        bit_depth = Controller((1, 16), 16)
        freq_hz = Controller((0, 44100), 44100)
        noise = Controller((0, 256), 0)
