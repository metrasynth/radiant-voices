from rv.structure.controller import Controller
from rv.structure.module import GenericModule


class AmplifierModule(GenericModule):

    class controller_types:
        volume = Controller(0x01, (0, 1024))
        panning = Controller(0x02, (-128, 128))
        dc_offset = Controller(0x03, (-128, 128))
        inverse = Controller(0x04, bool)
        stereo_width = Controller(0x05, (0, 256))
        absolute = Controller(0x06, bool)
        fine_volume = Controller(0x07, (0, 32768))
