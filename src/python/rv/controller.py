import logging
from enum import Enum

from rv.errors import ControllerValueError, RangeValidationError

log = logging.getLogger(__name__)


class Controller:
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

    def controller(self, instance):
        return self

    def instance_value_type(self, instance):
        if hasattr(self.value_type, "parent"):
            return self.value_type.parent(instance)
        else:
            return self.value_type

    def pattern_value(self, instance, value):
        """Convert a controller value to a pattern value (0x0000-0x8000)"""
        t = self.instance_value_type(instance)
        if isinstance(t, Range) and t.min == 0:
            shifted = value - t.min
            shifted_max = t.max - t.min
            return int(shifted / (shifted_max / 32768))
        else:
            return value

    def propagate(self, instance, value, down=False, up=False):
        self.set_initial(instance, value)
        callback = getattr(instance, "on_{}_changed".format(self.name), None)
        if callable(callback):
            callback(value, down=down, up=up)
        callback = getattr(instance, "on_controller_changed", None)
        if callable(callback):
            callback(self, value, down=down, up=up)

    def set_initial(self, instance, value):
        t = self.instance_value_type(instance)
        if isinstance(value, str) and isinstance(t, type) and issubclass(t, Enum):
            value = t[value]
        elif t is None:
            value = None
        else:
            try:
                value = t(value)
            except RangeValidationError as e:
                evalue, emin, emax = e.args
                raise ControllerValueError(
                    "{:x}({}).{}={} is not within [{}, {}]".format(
                        instance.index or 0,
                        instance.mtype,
                        self.name,
                        evalue,
                        emin,
                        emax,
                    )
                )
        instance.controller_values[self.name] = value


class Range:
    """Represents a valid range of values for a controller.

    Pass instances of `Range` to `Controller` in the `value_type` argument.
    """

    def __init__(self, min_value, max_value):
        self.min = min_value
        self.max = max_value

    def __call__(self, value):
        self.validate(value)
        return value

    def __eq__(self, other):
        return type(self) is type(other) and (self.min, self.max) == (
            other.min,
            other.max,
        )

    def __repr__(self):
        return "<{} {}..{}>".format(self.__class__.__name__, self.min, self.max)

    def from_raw_value(self, raw_value):
        return raw_value + self.min if self.min < 0 else raw_value

    def to_raw_value(self, value):
        return value - self.min if self.min < 0 else value

    def validate(self, value):
        if value < self.min or value > self.max:
            e = RangeValidationError(value, self.min, self.max)
            if isinstance(self, WarnOnlyRange):
                log.warning(str(e))
            else:
                raise e


class WarnOnlyRange(Range):
    pass


class CompactRange(Range):
    """Represents a compact range of values for a controller.

    Used to differentiate contollers such as MultiSynth.Transpose (discrete)
    and MultiSynth.Finetune (not discrete).

    Whereas Range is always shifted and scaled to 0x0000-0x8000 for the purposes of
    XXYY columns and min/max values in MultiCtls, CompactRange is only shifted.

    For example, the value -2 in the CompactRange(-128, 128) would be encoded
    as the value 126.
    """


class NoOffsetRange(Range):
    """Represents a range that does not adjust for negative min values.

    The raw values of VorbisPlayer.finetune are stored as signed ints.
    """

    def from_raw_value(self, raw_value):
        return raw_value

    def to_raw_value(self, value):
        return value


class DependentRange:
    def __init__(self, ctl_name, range_map, default):
        self.ctl_name = ctl_name
        self.range_map = range_map
        self.default = default

    def __repr__(self):
        return "<DependentRange (varies)>"

    def parent(self, instance):
        loaded = instance.controllers_loaded
        if not loaded or self.ctl_name not in loaded:
            return self.default
        else:
            ctl_val = instance.controller_values.get(self.ctl_name, None)
            if ctl_val is not None:
                return self.range_map[ctl_val]
            else:
                return self.default
