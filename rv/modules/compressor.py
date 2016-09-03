from enum import IntEnum

from rv.controller import Controller
from rv.modules import Module


class Compressor(Module):

    name = mtype = 'Compressor'
    mgroup = 'Effect'

    class Mode(IntEnum):
        PEAK = 0
        RMS = 1

    volume = Controller((0, 512) ,256)
    threshold = Controller((0, 512), 256)
    slope_pct = Controller((0, 200), 100)
    attack_ms = Controller((0, 500), 1)
    release_ms = Controller((1, 1000), 300)
    mode = Controller(Mode, Mode.PEAK)
    sidechain_input = Controller((0, 32), 0)
