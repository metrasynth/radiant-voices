from rv.structure.controller import Controller, Range
from rv.structure.module import GenericModule


class VorbisPlayerModule(GenericModule):

    # TODO: CHNK, CHNM, CHDT, CHFF, CHFR

    class controller_types:
        volume = Controller(0x01, Range(0, 512))
        original_speed = Controller(0x02, bool)
        finetune = Controller(0x03, Range(-128, 128))
        transpose = Controller(0x04, Range(-128, 128))
        interpolation = Controller(0x05, bool)
        polyphony_ch = Controller(0x06, Range(1, 4))
        repeat = Controller(0x07, bool)
