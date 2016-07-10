from rv.structure.controller import Controller
from rv.structure.module import GenericModule


class GpioModule(GenericModule):

    class controller_types:
        out = Controller(0x01, bool)
        out_pin = Controller(0x02, (0, 64))
        out_threshold = Controller(0x03, (0, 100))
        in_ = Controller(0x03, bool)
        in_pin = Controller(0x04, (0, 64))
        in_note = Controller(0x05, (0, 128))
        in_amplitude = Controller(0x06, (0, 100))
