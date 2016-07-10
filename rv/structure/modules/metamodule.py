from rv.structure.controller import Controller
from rv.structure.module import GenericModule


class MetamoduleModule(GenericModule):

    # TODO: CHNK, CHNM, CHDT, CHFF, CHFR

    class controller_types:
        volume = Controller(0x01, (0, 1024))
        input_module = Controller(0x02, (1, 256))
        play_patterns = Controller(0x03, bool)
        bpm = Controller(0x04, (1, 800))
        tpl = Controller(0x05, (1, 31))
        # TODO: user defined controllers
