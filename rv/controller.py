from enum import Enum

from rv.errors import ControllerValueError


class Controller(object):
    """Defines a type of controller attached to a module.

    In Module classes, define controllers in the order they are
    enumerated in SunVox, so that they receive the correct index.

    In Module instances, setting a named Controller's value
    will cause validation to occur.

    Validation is done by calling the Controller's `value_type`,
    which will raise a `ValueError` if not a valid enum value,
    or not within the specified range.
    """

    _next_order = 0

    name = None
    number = None

    def __init__(self, value_type, default, attached=True):
        if isinstance(value_type, tuple):
            value_type = Range(*value_type)
        self.value_type = value_type
        self.default = default
        self._attached = attached
        self._order = Controller._next_order
        Controller._next_order += 1

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return instance.controller_values[self.name]

    def __set__(self, instance, value):
        if instance is not None:
            self.propagate(instance, value, down=True, up=True)

    def attached(self, instance):
        return self._attached

    def pattern_value(self, value):
        """Convert a controller value to a pattern value (0x0000-0x8000)"""
        t = self.value_type
        if isinstance(t, Range) and t.min == 0:
            shifted = value - t.min
            shifted_max = t.max - t.min
            return int(shifted / (shifted_max / 32768))
        else:
            return value

    def propagate(self, instance, value, down=False, up=False):
        self.set_initial(instance, value)
        callback = getattr(instance, 'on_{}_changed'.format(self.name), None)
        if callable(callback):
            callback(value, down=down, up=up)
        callback = getattr(instance, 'on_controller_changed', None)
        if callable(callback):
            callback(self, value, down=down, up=up)

    def set_initial(self, instance, value):
        if isinstance(value, str) \
                and isinstance(self.value_type, type) \
                and issubclass(self.value_type, Enum):
            value = self.value_type[value]
        elif self.value_type is None:
            value = None
        else:
            value = self.value_type(value)
        instance.controller_values[self.name] = value


class Range(object):
    """Represents a valid range of values for a controller.

    Pass instances of `Range` to `Controller` in the `value_type` argument.
    """

    def __init__(self, min_value, max_value):
        self.min = min_value
        self.max = max_value

    def __call__(self, value):
        self.validate(value)
        return value

    def __repr__(self):
        return '<Range {}…{}>'.format(self.min, self.max)

    def from_raw_value(self, raw_value):
        return raw_value + self.min if self.min < 0 else raw_value

    def to_raw_value(self, value):
        return value - self.min if self.min < 0 else value

    def validate(self, value):
        if value < self.min or value > self.max:
            raise ControllerValueError('{} is not within [{}, {}]'.format(
                value, self.min, self.max))


class CompactRange(Range):
    """Represents a compact range of values for a controller.

    Used to differentiate contollers such as MultiSynth.Transpose (discrete)
    and MultiSynth.Finetune (not discrete).

    Whereas Range is always shifted and scaled to 0x0000-0x8000 for the purposes of
    XXYY columns and min/max values in MultiCtls, CompactRange is only scaled.

    For example, the value -2 in the CompactRange(-128, 128) would be encoded
    as the value 126.
    """
