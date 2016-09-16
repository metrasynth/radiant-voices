from rv.controller import Controller
from rv.modules import Module


class Amplifier(Module):

    name = mtype = 'Amplifier'
    mgroup = 'Effect'

    volume = Controller((0, 1024), 256)
    panning = Controller((-128, 128), 0)
    dc_offset = Controller((-128, 128), 0)
    inverse = Controller(bool, False)
    stereo_width = Controller((0, 256), 128)
    absolute = Controller(bool, False)
    fine_volume = Controller((0, 32768), 32768)