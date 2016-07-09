from enum import IntEnum
from importlib import import_module
import struct

from rv.lib.delegator import SimpleDelegator
from rv.structure.controller import Controller


class Module(object):

    def __init__(self):
        self.controller_values = []
        self.midi_inputs = MidiInputList()
        self.flags = 0
        self.type = None
        self.x, self.y, self.z = 0, 0, 0

    def specialized(self):
        if self.type is not None:
            type_name = self.type.replace(' ', '')
            class_name = type_name + 'Module'
            module_name = 'rv.structure.modules.{}'.format(type_name.lower())
            try:
                module = import_module(module_name)
            except ImportError:
                delegator = GenericModule
            else:
                delegator = getattr(module, class_name)
            return delegator(self)
        else:
            from .modules.output import OutputModule
            return OutputModule(self)

    def __getstate__(self):
        return dict(
            controller_values=self.controller_values,
            midi_inputs=self.midi_inputs,
            flags=self.flags,
            type=self.type,
            x=self.x,
            y=self.y,
            z=self.z,
        )


class MidiMessageType(IntEnum):

    UNSET = 0x00
    NOTE = 0x01
    KEY_PRESSURE = 0x02
    CONTROL_CHANGE = 0x03
    NRPN = 0x04
    RPN = 0x05
    PROGRAM_CHANGE = 0x06
    CHANNEL_PRESSURE = 0x07
    PITCH_BEND = 0x08


class MidiInputCurveType(IntEnum):

    LINEAR = 0x00
    INVERSE_LOG = 0x01
    LOG = 0x02
    S_CURVE = 0x03
    BINARY = 0x04
    TOGGLER = 0x05


class MidiInput(object):

    def __init__(self, data):
        (
            message_type,
            channel,
            curve_type,
            _,
            message_parameter,
            min_percent,
            max_percent,
        ) = struct.unpack('<BBBBHBB', data)
        self.message_type = MidiMessageType(message_type)
        self.message_parameter = message_parameter
        self.channel = channel
        self.curve_type = MidiInputCurveType(curve_type)
        self.min_percent = min_percent
        self.max_percent = min(max_percent, 200)

    def __getstate__(self):
        return dict(
            message_type=self.message_type.name,
            message_parameter=self.message_parameter,
            channel=self.channel,
            curve_type=self.curve_type.name,
            min_percent=self.min_percent,
            max_percent=self.max_percent,
        )


class MidiInputList(list):

    def append(self, obj):
        super(MidiInputList, self).append(MidiInput(obj))


class GenericModule(SimpleDelegator):

    class controllers(object):
        pass

    def __getattr__(self, name):
        controller_cls = getattr(self.controllers, name, None)
        if controller_cls is not None:
            i = controller_cls.index - 1
            return self.controller_values[i]
        else:
            return super(GenericModule, self).__getattr__(name)

    def __getstate__(self):
        return dict(
            self.delegate_sd_obj.__getstate__(),
            controllers=dict(
                (name, self.controller_values[controller_cls.index - 1])
                for name, controller_cls
                in self.controllers.__dict__.items()
                if isinstance(controller_cls, Controller)
            ),
        )
