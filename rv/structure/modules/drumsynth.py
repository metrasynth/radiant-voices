from rv.structure.controller import Controller
from rv.structure.module import GenericModule


class DrumsynthModule(GenericModule):

    class controller_types:
        volume = Controller(0x01, (0, 512))
        panning = Controller(0x02, (-128, 128))
        polyphony_ch = Controller(0x03, (1, 8))
        bass_volume = Controller(0x04, (0, 512))
        bass_power = Controller(0x05, (0, 256))
        bass_tone = Controller(0x06, (0, 256))
        bass_length = Controller(0x07, (0, 256))
        hihat_volume = Controller(0x08, (0, 512))
        hihat_length = Controller(0x09, (0, 256))
        snare_volume = Controller(0x0a, (0, 512))
        snare_tone = Controller(0x0b, (0, 256))
        snare_length = Controller(0x0c, (0, 256))
