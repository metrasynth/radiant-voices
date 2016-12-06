from enum import Enum

from rv.controller import Controller
from rv.modules import Behavior as B, Module


class Pitch2Ctl(Module):

    name = mtype = 'Pitch2Ctl'
    mgroup = 'Misc'

    behaviors = {B.receives_notes, B.sends_controls}

    class Mode(Enum):
        frequency_hz = 0
        pitch = 1

    class NoteOffAction(Enum):
        do_nothing = 0
        pitch_down = 1
        pitch_up = 2

    mode = Controller(Mode, Mode.frequency_hz)
    note_off_action = Controller(NoteOffAction, NoteOffAction.do_nothing)
    first_note = Controller((0, 256), 0)
    number_of_semitones = Controller((0, 256), 120)
    out_min = Controller((0, 32768), 0)
    out_max = Controller((0, 32768), 32768)
    out_controller = Controller((0, 32), 0)
