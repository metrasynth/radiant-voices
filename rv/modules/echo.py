from enum import Enum

from rv.controller import Controller
from rv.modules import Behavior as B, Module


class Echo(Module):

    name = mtype = 'Echo'
    mgroup = 'Effect'

    behaviors = {B.receives_audio, B.sends_audio}

    class Channels(Enum):
        mono = 0
        stereo = 1

    class DelayUnits(Enum):
        sec_256 = 0  # sec/256
        ms = 1
        hz = 2
        tick = 3
        line = 4
        line_2 = 5  # line/2
        line_3 = 6  # line/3

    dry = Controller((0, 256), 256)
    wet = Controller((0, 256), 128)
    feedback = Controller((0, 256), 128)
    delay = Controller((0, 256), 256)
    channels = Controller(Channels, Channels.stereo)
    delay_units = Controller(DelayUnits, DelayUnits.sec_256)
