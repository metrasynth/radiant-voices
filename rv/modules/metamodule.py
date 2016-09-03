from rv.controller import Controller
from rv.modules import Module


class MetaModule(Module):
    """
    In addition to standard controllers, you can assign zero or more
    user-defined controllers which map to module/controller pairs
    in the project embedded within the MetaModule.
    """

    name = mtype = 'MetaModule'
    mgroup = 'Misc'

    # TODO: CHNK, CHNM, CHDT, CHFF, CHFR

    volume = Controller((0, 1024), 256)
    input_module = Controller((1, 256), 1)
    play_patterns = Controller(bool, False)
    bpm = Controller((1, 800), 125)
    tpl = Controller((1, 31), 6)
    # TODO: user defined controllers


"""
CHNK: 00000010
CHFF: 00000000
CHFR: 00000000

CHNM: 0
CHDT: <contents of embedded SVOX>

CHNM: 1
CHDT: custom controller mappings (32); each having two shorts:
        bytes 0-1: module
        bytes 2-3: controller (0-based)

CHNM: 2
CHDT: options, 64 bytes:
        0: number of user defined ctls (0-27)
        1: arpeggiator
        2: apply velocity to project
        3-63: zero padding

CHNM: 8 + 0-based index of user defined control
CHDT: null-terminated string with custom label
"""
