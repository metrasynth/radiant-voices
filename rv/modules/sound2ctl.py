from enum import IntEnum

from rv.controller import Controller
from rv.modules import Module


class Sound2Ctl(Module):

    name = mtype = 'Sound2Ctl'
    mgroup = 'Misc'

    class Channels(IntEnum):
        MONO = 0
        STEREO = 1

    class Mode(IntEnum):
        LQ = 0
        HQ = 1

    # TODO: CHNK, CHNM, CHDT, CHFF, CHFR

    sample_rate_hz = Controller((1, 32768), 50)
    channels = Controller(Channels, Channels.MONO)
    absolute = Controller(bool, True)
    gain = Controller((0, 1024), 256)
    smooth = Controller((0, 256), 128)
    mode = Controller(Mode, Mode.HQ)
    out_min = Controller((0, 32768), 0)
    out_max = Controller((0, 32768), 32768)
    out_controller = Controller((0, 32), 0)


Channels = Sound2Ctl.Channels
Mode = Sound2Ctl.Mode


"""
"""


"""
CHNK: 00000010
CHNM: 0
CHDT: options, 64 bytes:
        0: record values
        1-63: zero padding
CHFF: 00000000
CHFR: 00000000
"""
