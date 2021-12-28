# -- DO NOT EDIT THIS FILE DIRECTLY --
"""
Base class for Echo
This file was auto-generated by genrv.
"""
from enum import IntEnum

from rv.controller import Controller, DependentRange, WarnOnlyRange


class BaseEcho:
    name = "Echo"
    mtype = "Echo"
    mgroup = "Effect"
    flags = 0x451

    class DelayUnit(IntEnum):
        sec_div_256 = 0
        ms = 1
        hz = 2
        tick = 3
        line = 4
        line_div_2 = 5
        line_div_3 = 6

    class Filter(IntEnum):
        off = 0
        lp_6db = 1
        hp_6db = 2

    dry = Controller((0, 256), 256)
    wet = Controller((0, 256), 40)
    feedback = Controller((0, 256), 128)
    delay = Controller(
        DependentRange(
            "delay_unit",
            {
                DelayUnit.sec_div_256: WarnOnlyRange(0, 256),
                DelayUnit.ms: WarnOnlyRange(0, 4000),
                DelayUnit.hz: WarnOnlyRange(0, 8192),
                DelayUnit.tick: WarnOnlyRange(0, 256),
                DelayUnit.line: WarnOnlyRange(0, 256),
                DelayUnit.line_div_2: WarnOnlyRange(0, 256),
                DelayUnit.line_div_3: WarnOnlyRange(0, 256),
            },
            WarnOnlyRange(0, 256),
        ),
        256,
    )
    right_channel_offset = Controller(bool, True)
    delay_unit = Controller(DelayUnit, DelayUnit.sec_div_256)
    right_channel_offset_length = Controller((0, 32768), 16384)
    filter = Controller(Filter, Filter.off)
    filter_freq = Controller((0, 22000), 2000)
