from rv.controller import Controller
from rv.modules import Behavior as B, Module


class Gpio(Module):

    name = mtype = 'GPIO'
    mgroup = 'Misc'

    behaviors = {B.receives_audio, B.sends_audio}

    out = Controller(bool, False)
    out_pin = Controller((0, 64), 0)
    out_threshold = Controller((0, 100), 50)
    in_ = Controller(bool, False)
    in_pin = Controller((0, 64), 0)
    in_note = Controller((0, 128), 0)
    in_amplitude = Controller((0, 100), 100)
