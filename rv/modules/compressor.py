from enum import Enum

from rv.controller import Controller
from rv.modules import Behavior as B, Module
from rv.modules.base.compressor import BaseCompressor


class Compressor(BaseCompressor, Module):

    flags = 0x002051

    behaviors = {B.receives_audio, B.sends_audio}

    class Mode(Enum):
        peak = 0
        rms = 1
        peak_zero_latency = 2

    volume = Controller((0, 512), 256)
    threshold = Controller((0, 512), 256)
    slope_pct = Controller((0, 200), 100)
    attack_ms = Controller((0, 500), 1)
    release_ms = Controller((1, 1000), 300)
    mode = Controller(Mode, Mode.peak)
    sidechain_input = Controller((0, 32), 0)
