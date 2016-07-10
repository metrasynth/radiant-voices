from enum import IntEnum

from rv.structure.controller import Controller
from rv.structure.module import GenericModule


class Type(IntEnum):

    LIM = 0
    SAT = 1


class DistortionModule(GenericModule):

    class controller_types:
        volume = Controller(0x01, (0, 256))
        type = Controller(0x02, Type)
        power = Controller(0x03, (0, 256))
        bit_depth = Controller(0x04, (1, 16))
        freq_hz = Controller(0x05, (0, 44100))
        noise = Controller(0x06, (0, 256))
