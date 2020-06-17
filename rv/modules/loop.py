from rv.controller import Controller
from rv.modules import Behavior as B, Module
from rv.modules.base.loop import BaseLoop


class Loop(BaseLoop, Module):

    flags = 0x000451

    behaviors = {B.receives_audio, B.sends_audio}

    Channels = BaseLoop.Channels
    Mode = BaseLoop.Mode

    volume = Controller((0, 256), 256)
    delay = Controller((0, 256), 256)  # line / 128
    channels = Controller(Channels, Channels.stereo)
    repeats = Controller((0, 64), 0)
    mode = Controller(Mode, Mode.normal)
