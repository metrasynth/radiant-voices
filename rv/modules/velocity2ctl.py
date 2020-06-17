from enum import Enum

from rv.controller import Controller
from rv.modules import Behavior as B, Module
from rv.modules.base.velocity2ctl import BaseVelocity2Ctl


class Velocity2Ctl(BaseVelocity2Ctl, Module):

    flags = 0x020049

    behaviors = {B.receives_notes, B.sends_controls}

    NoteOffAction = BaseVelocity2Ctl.NoteOffAction

    note_off_action = Controller(NoteOffAction, NoteOffAction.do_nothing)
    out_min = Controller((0, 32768), 0)
    out_max = Controller((0, 32768), 32768)
    out_offset = Controller((-16384, 16384), 0)
    out_controller = Controller((0, 32), 0)
