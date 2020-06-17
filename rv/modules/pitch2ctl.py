from rv.controller import Controller
from rv.modules import Behavior as B, Module
from rv.modules.base.pitch2ctl import BasePitch2Ctl


class Pitch2Ctl(BasePitch2Ctl, Module):

    flags = 0x020049

    behaviors = {B.receives_notes, B.sends_controls}

    Mode = BasePitch2Ctl.Mode
    NoteOffAction = BasePitch2Ctl.NoteOffAction

    mode = Controller(Mode, Mode.frequency_hz)
    note_off_action = Controller(NoteOffAction, NoteOffAction.do_nothing)
    first_note = Controller((0, 256), 0)
    number_of_semitones = Controller((0, 256), 120)
    out_min = Controller((0, 32768), 0)
    out_max = Controller((0, 32768), 32768)
    out_controller = Controller((0, 32), 0)
