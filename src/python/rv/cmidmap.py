from enum import Enum
from struct import pack, unpack


class MidiMessageType(Enum):
    unset = 0
    note = 1
    key_pressure = 2
    control_change = 3
    nrpn = 4
    rpn = 5
    program_change = 6
    channel_pressure = 7
    pitch_bend = 8


class Slope(Enum):
    linear = 0
    exp1 = 1
    exp2 = 2
    s_curve = 3
    cut = 4
    toggle = 5


class ControllerMidiMap:
    def __init__(self):
        self.channel = 0
        self.message_type = MidiMessageType.unset
        self.message_parameter = 0
        self.slope = Slope.linear

    @property
    def cmid_data(self):
        return pack(
            "<BBBBHBB",
            self.message_type.value,
            self.channel,
            self.slope.value,
            0,
            self.message_parameter,
            0,
            0xFF if self.message_type == MidiMessageType.unset else 0xC8,
        )

    @cmid_data.setter
    def cmid_data(self, data):
        message_type, self.channel, slope, _, self.message_parameter, _, _ = unpack(
            "<BBBBHBB", data
        )
        self.message_type = MidiMessageType(message_type)
        self.slope = Slope(slope)
