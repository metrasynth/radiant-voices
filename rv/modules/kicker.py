from enum import IntEnum

from rv.controller import Controller
from rv.module import Module


class Waveform(IntEnum):

    TRIANGLE = 0
    SQUARE = 1


class KickerModule(Module):

    name = mtype = 'Kicker'

    volume = Controller((0, 256), 256)
    waveform = Controller(Waveform, Waveform.TRIANGLE)
    panning = Controller((-128, 128), 0)
    attack = Controller((0, 512), 0)
    release = Controller((0, 512), 32)
    vol_addition = Controller((0, 1024), 0)
    env_acceleration = Controller((0, 1024), 256)
    polyphony_ch = Controller((1, 4), 1)
    anticlick = Controller(bool, False)
