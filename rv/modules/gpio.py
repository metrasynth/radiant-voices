from rv.controller import Controller
from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.gpio import BaseGpio


class Gpio(BaseGpio, Module):

    flags = 0x000051

    behaviors = {B.receives_audio, B.sends_audio}

    out = Controller(bool, False)
    out_pin = Controller((0, 256), 0)
    out_threshold = Controller((0, 100), 50)
    in_ = Controller(bool, False)
    in_pin = Controller((0, 256), 0)
    in_note = Controller((0, 128), 0)
    in_amplitude = Controller((0, 100), 100)
