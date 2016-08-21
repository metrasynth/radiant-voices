from enum import IntEnum

from rv.controller import Controller
from rv.modules import Module
from rv.modules import register


class Mode(IntEnum):

    PEAK = 0
    RMS = 1


@register
class CompressorModule(Module):

    type = name = 'Compressor'

    volume = Controller((0, 512) ,256)
    threshold = Controller((0, 512), 256)
    slope_pct = Controller((0, 200), 100)
    attack_ms = Controller((0, 500), 1)
    release_ms = Controller((1, 1000), 300)
    mode = Controller(Mode, Mode.PEAK)
    sidechain_input = Controller((0, 32), 0)
