from rv.structure.controller import Controller
from rv.structure.module import GenericModule


class MultictlModule(GenericModule):

    # TODO: CHNK, CHNM, CHDT, CHFF, CHFR

    class controller_types:
        value = Controller(0x01, (0, 32768))
        gain = Controller(0x02, (0, 1024))
        quantization = Controller(0x03, (0, 32768))
