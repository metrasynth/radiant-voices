from enum import IntEnum
from struct import pack, unpack

from attr import attr, attributes
from rv.errors import ModuleOwnershipError, PatternOwnershipError
from rv.lib.validators import in_range
from rv.modules.module import Module


class NOTE(IntEnum):
    """All notes available for patterns or mapping."""

    (
        C0,
        c0,
        D0,
        d0,
        E0,
        F0,
        f0,
        G0,
        g0,
        A0,
        a0,
        B0,
        C1,
        c1,
        D1,
        d1,
        E1,
        F1,
        f1,
        G1,
        g1,
        A1,
        a1,
        B1,
        C2,
        c2,
        D2,
        d2,
        E2,
        F2,
        f2,
        G2,
        g2,
        A2,
        a2,
        B2,
        C3,
        c3,
        D3,
        d3,
        E3,
        F3,
        f3,
        G3,
        g3,
        A3,
        a3,
        B3,
        C4,
        c4,
        D4,
        d4,
        E4,
        F4,
        f4,
        G4,
        g4,
        A4,
        a4,
        B4,
        C5,
        c5,
        D5,
        d5,
        E5,
        F5,
        f5,
        G5,
        g5,
        A5,
        a5,
        B5,
        C6,
        c6,
        D6,
        d6,
        E6,
        F6,
        f6,
        G6,
        g6,
        A6,
        a6,
        B6,
        C7,
        c7,
        D7,
        d7,
        E7,
        F7,
        f7,
        G7,
        g7,
        A7,
        a7,
        B7,
        C8,
        c8,
        D8,
        d8,
        E8,
        F8,
        f8,
        G8,
        g8,
        A8,
        a8,
        B8,
        C9,
        c9,
        D9,
        d9,
        E9,
        F9,
        f9,
        G9,
        g9,
        A9,
        a9,
        B9,
    ) = range(1, 121)


ALL_NOTES = set(NOTE)


class NOTECMD(IntEnum):
    """All notes and commands available for patterns."""

    (
        C0,
        c0,
        D0,
        d0,
        E0,
        F0,
        f0,
        G0,
        g0,
        A0,
        a0,
        B0,
        C1,
        c1,
        D1,
        d1,
        E1,
        F1,
        f1,
        G1,
        g1,
        A1,
        a1,
        B1,
        C2,
        c2,
        D2,
        d2,
        E2,
        F2,
        f2,
        G2,
        g2,
        A2,
        a2,
        B2,
        C3,
        c3,
        D3,
        d3,
        E3,
        F3,
        f3,
        G3,
        g3,
        A3,
        a3,
        B3,
        C4,
        c4,
        D4,
        d4,
        E4,
        F4,
        f4,
        G4,
        g4,
        A4,
        a4,
        B4,
        C5,
        c5,
        D5,
        d5,
        E5,
        F5,
        f5,
        G5,
        g5,
        A5,
        a5,
        B5,
        C6,
        c6,
        D6,
        d6,
        E6,
        F6,
        f6,
        G6,
        g6,
        A6,
        a6,
        B6,
        C7,
        c7,
        D7,
        d7,
        E7,
        F7,
        f7,
        G7,
        g7,
        A7,
        a7,
        B7,
        C8,
        c8,
        D8,
        d8,
        E8,
        F8,
        f8,
        G8,
        g8,
        A8,
        a8,
        B8,
        C9,
        c9,
        D9,
        d9,
        E9,
        F9,
        f9,
        G9,
        g9,
        A9,
        a9,
        B9,
    ) = range(1, 121)

    EMPTY = 0
    NOTE_OFF = 128
    ALL_NOTES_OFF = 129  # notes of all synths off
    CLEAN_SYNTHS = 130  # stop and clean all synths
    STOP = 131
    PLAY = 132
    SET_PITCH = 133
    PREV_TRACK = 134


class PatternEffect(IntEnum):
    """Effects available for the EE effect column."""

    SLIDE_UP = 0x01
    SLIDE_DOWN = 0x02
    SLIDE_TO_NOTE = 0x03
    VIBRATO = 0x04
    ARPEGGIO = 0x08
    SET_SAMPLE_OFFSET = 0x09
    SET_SAMPLE_OFFSET_BY_PERCENTAGE = 0x07
    SLIDE_VELOCITY_UP_DOWN = 0x0A
    SET_PLAYING_SPEED = 0x0F
    FINESLIDE_UP = 0x11
    FINESLIDE_DOWN = 0x12
    SET_BYPASS_SOLO_MUTE_FLAGS = 0x13
    RESET_BYPASS_SOLO_MUTE_FLAGS = 0x14
    CHANGE_RELATIVE_NOTE_XX_AND_FINETUNE_YY = 0x15
    RETRIGGER = 0x19
    CUT = 0x1C
    DELAY = 0x1D
    SET_BPM_TO_XXYY = 0x1F
    NOTE_PROBABILITY = 0x20
    NOTE_PROBABILITY_WITH_RANDOM_VELOCITY = 0x21
    WRITE_RANDOM_VALUE_0_XXYY_TO_CONTROLLER = 0x22
    WRITE_RANDOM_VALUE_XX_YY_TO_CONTROLLER = 0x23
    NOTE_FROM_LINE_XXYY = 0x24
    RANDOM_NOTE_FROM_LINE_XX_YY = 0x25
    NOTE_FROM_TRACK_XXYY = 0x26
    RANDOM_NOTE_FROM_TRACK_XX_YY = 0x27
    NOTE_FROM_LINE_XXYY_ON_TRACK_0 = 0x28
    RANDOM_NOTE_FROM_LINE_XX_YY_ON_TRACK_0 = 0x29
    STOP_PLAYING = 0x30
    JUMP_TO_LINE_XXYY = 0x31
    SET_JUMP_ADDRESS_MODE = 0x32
    DELETE_EVENT_ON_TRACK_XX_WITH_PROBABILITY_YY = 0x38
    CYCLIC_SHIFT_TRACK_DOWN_BY_YY_LINES = 0x39
    GENERATE_NEW_ITERATION_OF_YY_LINE_POLYRHYTHM_ON_TRACK_XX = 0x3A
    COPY_TRACK_XX_TO_PATTERN_NAMED_YY = 0x3B
    DELAY_EVENT_FOR_0x00_PCT_OF_LINE = 0x40
    DELAY_EVENT_FOR_0x01_PCT_OF_LINE = 0x41
    DELAY_EVENT_FOR_0x02_PCT_OF_LINE = 0x42
    DELAY_EVENT_FOR_0x03_PCT_OF_LINE = 0x43
    DELAY_EVENT_FOR_0x04_PCT_OF_LINE = 0x44
    DELAY_EVENT_FOR_0x05_PCT_OF_LINE = 0x45
    DELAY_EVENT_FOR_0x06_PCT_OF_LINE = 0x46
    DELAY_EVENT_FOR_0x07_PCT_OF_LINE = 0x47
    DELAY_EVENT_FOR_0x08_PCT_OF_LINE = 0x48
    DELAY_EVENT_FOR_0x09_PCT_OF_LINE = 0x49
    DELAY_EVENT_FOR_0x0A_PCT_OF_LINE = 0x4A
    DELAY_EVENT_FOR_0x0B_PCT_OF_LINE = 0x4B
    DELAY_EVENT_FOR_0x0C_PCT_OF_LINE = 0x4C
    DELAY_EVENT_FOR_0x0D_PCT_OF_LINE = 0x4D
    DELAY_EVENT_FOR_0x0E_PCT_OF_LINE = 0x4E
    DELAY_EVENT_FOR_0x0F_PCT_OF_LINE = 0x4F
    DELAY_EVENT_FOR_0x10_PCT_OF_LINE = 0x50
    DELAY_EVENT_FOR_0x11_PCT_OF_LINE = 0x51
    DELAY_EVENT_FOR_0x12_PCT_OF_LINE = 0x52
    DELAY_EVENT_FOR_0x13_PCT_OF_LINE = 0x53
    DELAY_EVENT_FOR_0x14_PCT_OF_LINE = 0x54
    DELAY_EVENT_FOR_0x15_PCT_OF_LINE = 0x55
    DELAY_EVENT_FOR_0x16_PCT_OF_LINE = 0x56
    DELAY_EVENT_FOR_0x17_PCT_OF_LINE = 0x57
    DELAY_EVENT_FOR_0x18_PCT_OF_LINE = 0x58
    DELAY_EVENT_FOR_0x19_PCT_OF_LINE = 0x59
    DELAY_EVENT_FOR_0x1A_PCT_OF_LINE = 0x5A
    DELAY_EVENT_FOR_0x1B_PCT_OF_LINE = 0x5B
    DELAY_EVENT_FOR_0x1C_PCT_OF_LINE = 0x5C
    DELAY_EVENT_FOR_0x1D_PCT_OF_LINE = 0x5D
    DELAY_EVENT_FOR_0x1E_PCT_OF_LINE = 0x5E
    DELAY_EVENT_FOR_0x1F_PCT_OF_LINE = 0x5F


@attributes(slots=True)
class Note:
    """A single note, for use within a :py:class:`Pattern`."""

    note = attr(converter=NOTECMD, default=NOTECMD.EMPTY)
    vel = attr(converter=int, validator=in_range(0, 129), default=0)
    module = attr(converter=int, validator=in_range(0, 0xFFFF), default=0)
    ctl = attr(converter=int, validator=in_range(0, 0xFFFF), default=0)
    val = attr(converter=int, validator=in_range(0, 0xFFFF), default=0)
    pattern = attr(default=None)

    def __str__(self):
        tokens = [
            "%s%i" % (attr[0], getattr(self, attr))
            for attr in ["note", "vel", "ctl", "val"]
            if hasattr(self, attr)
        ]

        return "".join(tokens)

    @property
    def project(self):
        return self.pattern.project

    @property
    def module_index(self):
        return None if self.module == 0 else self.module - 1

    @property
    def mod(self):
        if self.project is None:
            raise PatternOwnershipError("Pattern not owned by a project")
        if self.module_index is None:
            return None
        elif self.module_index < len(self.project.modules):
            return self.project.modules[self.module_index]

    @mod.setter
    def mod(self, new_mod: Module):
        if new_mod.parent is None:
            raise ModuleOwnershipError("Module must be attached to a project")
        self.module = new_mod.index + 1

    @property
    def controller(self):
        return self.ctl >> 8

    @controller.setter
    def controller(self, value):
        self.ctl |= (value & 0xFF) << 8

    @property
    def effect(self):
        return self.ctl & 0xFF

    @effect.setter
    def effect(self, value):
        self.ctl |= value & 0xFF

    @property
    def val_xx(self):
        return self.val >> 8

    @val_xx.setter
    def val_xx(self, value):
        self.val |= (value & 0xFF) << 8

    @property
    def val_yy(self):
        return self.val & 0xFF

    @val_yy.setter
    def val_yy(self, value):
        self.val |= value & 0xFF

    @property
    def raw_data(self):
        return pack("<BBHHH", self.note, self.vel, self.module, self.ctl, self.val)

    @raw_data.setter
    def raw_data(self, raw_data):
        self.note, self.vel, self.module, self.ctl, self.val = unpack(
            "<BBHHH", raw_data
        )

    def clone(self):
        note = self.__class__()
        for name in ["note", "vel", "module", "ctl", "val"]:
            setattr(note, name, getattr(self, name))
        return note

    def is_empty(self):
        return not (self.note or self.vel or self.ctl or self.val)

    def tabular_repr(self, is_on=False, note_fmt="NN VV MMMM CC EE XXYY"):
        if self.note == NOTECMD.NOTE_OFF:
            nn = "=="
        elif self.note == NOTECMD.PREV_TRACK:
            nn = "<<"
        elif self.note == NOTECMD.SET_PITCH:
            nn = "SP"
        elif self.note == NOTECMD.EMPTY:
            nn = "//" if is_on else ".."
        else:
            nn = NOTECMD(self.note).name
        vv = "  " if self.vel == 0 else "{:02X}".format(self.vel - 1)
        mmmm = "    " if self.module == 0 else "{:04X}".format(self.module - 1)
        if self.controller or self.effect:
            cc = "{:02X}".format(self.controller)
            ee = "{:02X}".format(self.effect)
        else:
            cc = "  "
            ee = "  "
        if self.val_xx or self.val_yy:
            xx = "{:02X}".format(self.val_xx)
            yy = "{:02X}".format(self.val_yy)
        else:
            xx = "  "
            yy = "  "
        return (
            note_fmt.replace("NN", nn)
            .replace("VV", vv)
            .replace("MMMM", mmmm)
            .replace("CC", cc)
            .replace("EE", ee)
            .replace("XX", xx)
            .replace("YY", yy)
        )
