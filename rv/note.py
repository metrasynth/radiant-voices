from enum import IntEnum
from struct import pack, unpack

from attr import attr, attributes

from rv.lib.validators import in_range


class NOTE(IntEnum):
    """All notes available for patterns or mapping."""

    (C0, c0, D0, d0, E0, F0, f0, G0, g0, A0, a0, B0,
     C1, c1, D1, d1, E1, F1, f1, G1, g1, A1, a1, B1,
     C2, c2, D2, d2, E2, F2, f2, G2, g2, A2, a2, B2,
     C3, c3, D3, d3, E3, F3, f3, G3, g3, A3, a3, B3,
     C4, c4, D4, d4, E4, F4, f4, G4, g4, A4, a4, B4,
     C5, c5, D5, d5, E5, F5, f5, G5, g5, A5, a5, B5,
     C6, c6, D6, d6, E6, F6, f6, G6, g6, A6, a6, B6,
     C7, c7, D7, d7, E7, F7, f7, G7, g7, A7, a7, B7,
     C8, c8, D8, d8, E8, F8, f8, G8, g8, A8, a8, B8,
     C9, c9, D9, d9, E9, F9, f9, G9, g9, A9, a9, B9) = range(1, 121)

ALL_NOTES = set(NOTE)


class NOTECMD(IntEnum):
    """All notes and commands available for patterns."""

    (C0, c0, D0, d0, E0, F0, f0, G0, g0, A0, a0, B0,
     C1, c1, D1, d1, E1, F1, f1, G1, g1, A1, a1, B1,
     C2, c2, D2, d2, E2, F2, f2, G2, g2, A2, a2, B2,
     C3, c3, D3, d3, E3, F3, f3, G3, g3, A3, a3, B3,
     C4, c4, D4, d4, E4, F4, f4, G4, g4, A4, a4, B4,
     C5, c5, D5, d5, E5, F5, f5, G5, g5, A5, a5, B5,
     C6, c6, D6, d6, E6, F6, f6, G6, g6, A6, a6, B6,
     C7, c7, D7, d7, E7, F7, f7, G7, g7, A7, a7, B7,
     C8, c8, D8, d8, E8, F8, f8, G8, g8, A8, a8, B8,
     C9, c9, D9, d9, E9, F9, f9, G9, g9, A9, a9, B9) = range(1, 121)

    EMPTY = 0
    NOTE_OFF = 128
    ALL_NOTES_OFF = 129  # notes of all synths off
    CLEAN_SYNTHS = 130  # stop and clean all synths
    STOP = 131
    PLAY = 132
    SET_PITCH = 133
    PREV_TRACK = 134


@attributes(slots=True)
class Note(object):
    """A single note, for use within a :py:class:`Pattern`."""

    note = attr(convert=NOTECMD, default=NOTECMD.EMPTY)
    vel = attr(convert=int, validator=in_range(0, 129), default=0)
    module = attr(convert=int, validator=in_range(0, 0xff), default=0)
    ctl = attr(convert=int, validator=in_range(0, 0xffff), default=0)
    val = attr(convert=int, validator=in_range(0, 0xffff), default=0)

    @property
    def controller(self):
        return self.ctl >> 8

    @controller.setter
    def controller(self, value):
        self.ctl |= (value & 0xff) << 8

    @property
    def effect(self):
        return self.ctl & 0xff

    @effect.setter
    def effect(self, value):
        self.ctl |= value & 0xff

    @property
    def val_xx(self):
        return self.val >> 8

    @val_xx.setter
    def val_xx(self, value):
        self.val |= (value & 0xff) << 8

    @property
    def val_yy(self):
        return self.val & 0xff

    @val_yy.setter
    def val_yy(self, value):
        self.val |= value & 0xff

    @property
    def raw_data(self):
        return pack('<BBBBHH', self.note, self.vel, self.module, 0, self.ctl,
                    self.val)

    @raw_data.setter
    def raw_data(self, raw_data):
        self.note, self.vel, self.module, _, self.ctl, self.val = \
            unpack('<BBBBHH', raw_data)

    def tabular_repr(self, is_on=False, note_fmt='NN VV MM CC EE XXYY'):
        if self.note == NOTECMD.NOTE_OFF:
            nn = '=='
        elif self.note == NOTECMD.PREV_TRACK:
            nn = '<<'
        elif self.note == NOTECMD.SET_PITCH:
            nn = 'SP'
        elif self.note == NOTECMD.EMPTY:
            nn = '//' if is_on else '..'
        else:
            nn = NOTECMD(self.note).name
        if self.vel == 0:
            vv = '  '
        else:
            vv = '{:02X}'.format(self.vel - 1)
        if self.module == 0:
            mm = '  '
        else:
            mm = '{:02X}'.format(self.module - 1)
        if self.controller or self.effect:
            cc = '{:02X}'.format(self.controller)
            ee = '{:02X}'.format(self.effect)
        else:
            cc = '  '
            ee = '  '
        if self.val_xx or self.val_yy:
            xx = '{:02X}'.format(self.val_xx)
            yy = '{:02X}'.format(self.val_yy)
        else:
            xx = '  '
            yy = '  '
        return (
            note_fmt
            .replace('NN', nn)
            .replace('VV', vv)
            .replace('MM', mm)
            .replace('CC', cc)
            .replace('EE', ee)
            .replace('XX', xx)
            .replace('YY', yy)
        )
