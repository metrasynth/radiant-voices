from enum import IntEnum

from rv.structure.controller import Controller
from rv.structure.module import GenericModule


class MultisynthModule(GenericModule):

    # TODO: CHNK, CHNM, CHDT, CHFF, CHFR

    class controller_types:
        transpose = Controller(0x01, (-128, 128))
        random_pitch = Controller(0x02, (0, 4096))
        velocity = Controller(0x03, (0, 256))
        finetune = Controller(0x04, (-256, 256))
        random_phase = Controller(0x05, (0, 32768))
        random_velocity = Controller(0x06, (0, 32768))
        phase = Controller(0x07, (0, 32768))
