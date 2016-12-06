from rv.controller import Controller
from rv.modules import Behavior as B, Module


class Glide(Module):

    name = mtype = 'Glide'
    mgroup = 'Misc'

    behaviors = {B.receives_notes, B.sends_notes}

    response = Controller((0, 1000), 500)
    sample_rate_hz = Controller((1, 32768), 150)
    offset_on_1st_note = Controller(bool, False)
    polyphony = Controller(bool, True)
    pitch = Controller((-600, 600), 0)
    pitch_scale = Controller((0, 200), 100)
    reset = Controller(bool, False)  # used to reset module
