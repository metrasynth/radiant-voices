from enum import Enum

from rv.controller import Controller
from rv.modules import Behavior as B, Module


class Velocity2Ctl(Module):

    name = mtype = 'Velocity2Ctl'
    mgroup = 'Misc'

    behaviors = {B.receives_notes, B.sends_controls}

    class NoteOffAction(Enum):
        do_nothing = 0
        vel_down = 1
        vel_up = 2

    note_off_action = Controller(NoteOffAction, NoteOffAction.do_nothing)
    out_min = Controller((0, 32768), 0)
    out_max = Controller((0, 32768), 32768)
    out_offset = Controller((-16384, 16384), 0)
    out_controller = Controller((0, 32), 0)
