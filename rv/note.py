from enum import IntEnum
from struct import pack, unpack

from attr import attr, attributes

from rv.lib.validators import in_range


class NOTECMD(IntEnum):
    (C0, d0, D0, e0, E0, F0, G0, a0, A0, b0, B0,
     C1, d1, D1, e1, E1, F1, G1, a1, A1, b1, B1,
     C2, d2, D2, e2, E2, F2, G2, a2, A2, b2, B2,
     C3, d3, D3, e3, E3, F3, G3, a3, A3, b3, B3,
     C4, d4, D4, e4, E4, F4, G4, a4, A4, b4, B4,
     C5, d5, D5, e5, E5, F5, G5, a5, A5, b5, B5,
     C6, d6, D6, e6, E6, F6, G6, a6, A6, b6, B6,
     C7, d7, D7, e7, E7, F7, G7, a7, A7, b7, B7,
     C8, d8, D8, e8, E8, F8, G8, a8, A8, b8, B8,
     C9, d9, D9, e9, E9, F9, G9, a9, A9, b9, B9) = range(1, 111)
    EMPTY = 0
    NOTE_OFF = 128
    ALL_NOTES_OFF = 129  # notes of all synths off
    CLEAN_SYNTHS = 130  # stop and clean all synths
    STOP = 131
    PLAY = 132


@attributes(slots=True)
class Note(object):

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

    def tabular_repr(self):
        return repr(self.note)
