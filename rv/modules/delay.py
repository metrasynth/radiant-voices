from rv.controller import Controller
from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.delay import BaseDelay


class Delay(BaseDelay, Module):

    flags = 0x000451

    behaviors = {B.receives_audio, B.sends_audio}

    Channels = BaseDelay.Channels
    DelayUnits = BaseDelay.DelayUnits

    dry = Controller((0, 512), 256)
    wet = Controller((0, 512), 256)
    delay_l = Controller((0, 256), 128)
    delay_r = Controller((0, 256), 160)
    volume_l = Controller((0, 256), 256)
    volume_r = Controller((0, 256), 256)
    channels = Controller(Channels, Channels.stereo)
    inverse = Controller(bool, False)
    delay_units = Controller(DelayUnits, DelayUnits.sec_16384)
