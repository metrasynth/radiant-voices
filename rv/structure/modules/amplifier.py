from rv.structure.controller import Controller, Range
from rv.structure.module import GenericModule


class AmplifierModule(GenericModule):

    class controllers(object):
        volume = Controller(0x01, Range(0, 1024))
        panning = Controller(0x02, Range(-128, 128))
        dc_offset = Controller(0x03, Range(-128, 128))
        inverse = Controller(0x04, bool)
        stereo_width = Controller(0x05, Range(0, 256))
        absolute = Controller(0x06, bool)
        fine_volume = Controller(0x07, Range(0, 32768))
