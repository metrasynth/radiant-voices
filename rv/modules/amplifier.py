from rv.controller import Controller
from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.amplifier import BaseAmplifier


class Amplifier(BaseAmplifier, Module):

    flags = 0x000051

    behaviors = {B.receives_audio, B.sends_audio}

    receives_audio = True
    sends_audio = True

    volume = Controller((0, 1024), 256)
    panning = Controller((-128, 128), 0)
    dc_offset = Controller((-128, 128), 0)
    inverse = Controller(bool, False)
    stereo_width = Controller((0, 256), 128)
    absolute = Controller(bool, False)
    fine_volume = Controller((0, 32768), 32768)
    gain = Controller((0, 5000), 1)
