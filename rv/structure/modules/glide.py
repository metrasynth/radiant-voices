from rv.structure.controller import Controller
from rv.structure.module import GenericModule


class GlideModule(GenericModule):

    class controller_types:
        response = Controller(0x01, (0, 1000))
        sample_rate_hz = Controller(0x02, (1, 32768))
        offset_on_1st_note = Controller(0x03, bool)
        polyphony = Controller(0x04, bool)
        pitch = Controller(0x05, (-600, 600))
        pitch_scale = Controller(0x06, (0, 200))
        reset = Controller(0x07, bool)      # used to reset module
