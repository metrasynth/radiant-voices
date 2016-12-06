from enum import Enum

from rv.controller import Controller
from rv.modules import Behavior as B, Module


class Delay(Module):

    name = mtype = 'Delay'
    mgroup = 'Effect'

    behaviors = {B.receives_audio, B.sends_audio}

    class Channels(Enum):
        stereo = 0
        mono = 1

    class DelayUnits(Enum):
        sec_16384 = 0  # sec/16384
        ms = 1
        hz = 2
        tick = 3
        line = 4
        line_2 = 5  # line/2
        line_3 = 6  # line/3

    dry = Controller((0, 512), 256)
    wet = Controller((0, 512), 256)
    delay_l = Controller((0, 256), 128)
    delay_r = Controller((0, 256), 160)
    volume_l = Controller((0, 256), 256)
    volume_r = Controller((0, 256), 256)
    channels = Controller(Channels, Channels.stereo)
    inverse = Controller(bool, False)
    delay_units = Controller(DelayUnits, DelayUnits.sec_16384)
