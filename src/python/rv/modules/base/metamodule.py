# -- DO NOT EDIT THIS FILE DIRECTLY --
"""
Base class for MetaModule
This file was auto-generated by genrv.
"""
from enum import IntEnum

from rv.controller import Controller
from rv.option import Option


class BaseMetaModule:
    name = "MetaModule"
    mtype = "MetaModule"
    mgroup = "Misc"
    flags = default_flags = 0x8051

    class PlayPatterns(IntEnum):
        off = 0
        on_repeat = 1
        on_no_repeat = 2
        on_repeat_endless = 3
        on_no_repeat_endless = 4

    volume = Controller((0, 1024), 256)
    input_module = Controller((1, 256), 1)
    play_patterns = Controller(PlayPatterns, PlayPatterns.off)
    bpm = Controller((1, 1000), 125)
    tpl = Controller((1, 31), 6)
    user_defined_controllers = Option(
        name="user_defined_controllers",
        byte=0,
        bit=0,
        size=8,
        default=0,
    )
    arpeggiator = Option(
        name="arpeggiator",
        number=127,
        byte=1,
        bit=0,
        size=1,
        default=False,
    )
    apply_velocity_to_project = Option(
        name="apply_velocity_to_project",
        number=126,
        byte=2,
        bit=0,
        size=1,
        default=False,
    )
    event_output = Option(
        name="event_output",
        number=125,
        byte=3,
        bit=0,
        size=1,
        inverted=True,
        default=True,
    )
    receive_notes_from_keyboard = Option(
        name="receive_notes_from_keyboard",
        number=123,
        byte=4,
        bit=0,
        size=1,
        exclusive_of=["do_not_receive_notes_from_keyboard"],
        default=False,
    )
    do_not_receive_notes_from_keyboard = Option(
        name="do_not_receive_notes_from_keyboard",
        number=123,
        byte=4,
        bit=1,
        size=1,
        exclusive_of=["receive_notes_from_keyboard"],
        default=False,
    )
    auto_bpm_tpl = Option(
        name="auto_bpm_tpl",
        number=122,
        byte=4,
        bit=2,
        size=1,
        default=False,
    )
    ignore_eff_31_after_last_note_off = Option(
        name="ignore_eff_31_after_last_note_off",
        number=121,
        byte=4,
        bit=3,
        size=1,
        default=False,
    )
    jump_to_rl_pattern_after_last_note_off = Option(
        name="jump_to_rl_pattern_after_last_note_off",
        number=120,
        byte=4,
        bit=4,
        size=1,
        default=False,
    )
    dummy5 = Option(
        name="dummy5",
        byte=5,
        bit=0,
        size=1,
        default=False,
    )
    dummy6 = Option(
        name="dummy6",
        byte=6,
        bit=0,
        size=1,
        default=False,
    )
    dummy7 = Option(
        name="dummy7",
        byte=7,
        bit=0,
        size=1,
        default=False,
    )
