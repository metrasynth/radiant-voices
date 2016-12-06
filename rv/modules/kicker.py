from enum import Enum

from rv.controller import Controller
from rv.modules import Behavior as B, Module


class Kicker(Module):

    name = mtype = 'Kicker'
    mgroup = 'Synth'

    behaviors = {B.receives_notes, B.sends_audio}

    class Waveform(Enum):
        triangle = 0
        square = 1
        sin = 2

    volume = Controller((0, 256), 256)
    waveform = Controller(Waveform, Waveform.triangle)
    panning = Controller((-128, 128), 0)
    attack = Controller((0, 512), 0)
    release = Controller((0, 512), 32)
    vol_addition = Controller((0, 1024), 0)
    env_acceleration = Controller((0, 1024), 256)
    polyphony_ch = Controller((1, 4), 1)
    anticlick = Controller(bool, False)
