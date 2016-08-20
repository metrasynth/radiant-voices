from rv.controller import Controller
from rv.module import Module


class GpioModule(Module):

    name = mtype = 'GPIO'

    out = Controller(bool, False)
    out_pin = Controller((0, 64), 0)
    out_threshold = Controller((0, 100), 50)
    in_ = Controller(bool, False)
    in_pin = Controller((0, 64), 0)
    in_note = Controller((0, 128), 0)
    in_amplitude = Controller((0, 100), 100)
