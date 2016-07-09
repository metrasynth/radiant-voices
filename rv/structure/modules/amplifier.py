from rv.structure.controller import Controller, Choices, OnOff, Range
from rv.structure.module import GenericModule


class AmplifierModule(GenericModule):

    class controllers(object):

        volume = Controller(
            0x01, 'Volume', 0, 1024, Range(0, 1024))

        panning = Controller(
            0x02, 'Panning', 0, 256, Range(-128, 128))

        dc_offset = Controller(
            0x03, 'DC Offset', 0, 256, Range(-128, 128))

        inverse = Controller(
            0x04, 'Inverse', 0, 1, OnOff())

        stereo_width = Controller(
            0x05, 'Stereo width', 0, 256, Range(0, 256))

        absolute = Controller(
            0x06, 'Absolute', 0, 1, OnOff())

        fine_volume = Controller(
            0x07, 'Fine volume', 0, 0x8000, Range(0, 0x8000))
