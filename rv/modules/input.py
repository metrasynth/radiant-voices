from enum import Enum

from rv.controller import Controller
from rv.modules import Behavior as B, Module
from rv.modules.base.input import BaseInput


class Input(BaseInput, Module):

    flags = 0x000049

    behaviors = {B.sends_audio}

    Channels = BaseInput.Channels

    volume = Controller((0, 1024), 256)
    channels = Controller(Channels, Channels.mono)
