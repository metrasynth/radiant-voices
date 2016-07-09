from rv.structure.controller import Controller, Range
from rv.structure.module import GenericModule


class DrumsynthModule(GenericModule):

    class controllers(object):
        volume = Controller(0x01, Range(0, 512))
        panning = Controller(0x02, Range(-128, 128))
        polyphony_ch = Controller(0x03, Range(1, 8))
        bass_volume = Controller(0x04, Range(0, 512))
        bass_power = Controller(0x05, Range(0, 256))
        bass_tone = Controller(0x06, Range(0, 256))
        bass_length = Controller(0x07, Range(0, 256))
        hihat_volume = Controller(0x08, Range(0, 512))
        hihat_length = Controller(0x09, Range(0, 256))
        snare_volume = Controller(0x0a, Range(0, 512))
        snare_tone = Controller(0x0b, Range(0, 256))
        snare_length = Controller(0x0c, Range(0, 256))
