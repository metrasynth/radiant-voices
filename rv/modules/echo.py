from rv.controller import Controller
from rv.modules import Behavior as B, Module
from rv.modules.base.echo import BaseEcho


class Echo(BaseEcho, Module):

    flags = 0x000451

    behaviors = {B.receives_audio, B.sends_audio}

    Channels = BaseEcho.Channels
    DelayUnits = BaseEcho.DelayUnits

    dry = Controller((0, 256), 256)
    wet = Controller((0, 256), 128)
    feedback = Controller((0, 256), 128)
    delay = Controller((0, 256), 256)
    channels = Controller(Channels, Channels.stereo)
    delay_units = Controller(DelayUnits, DelayUnits.sec_256)
