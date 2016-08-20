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

    def __init__(self, value_type, default):
        if isinstance(value_type, tuple):
            value_type = Range(*value_type)
        self.value_type = value_type
        self.default = default
        self._order = Controller._next_order
        Controller._next_order += 1

    def __get__(self, instance, owner):
        return instance.controller_values[self.name]

    def __set__(self, instance, value):
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

    def from_raw_value(self, raw_value):
        return raw_value + self.min if self.min < 0 else raw_value

    def to_raw_value(self, value):
        return value - self.min if self.min < 0 else value

    def validate(self, value):
        if value < self.min or value > self.max:
            raise ValueError('{} is not within [{}, {}]'.format(
                value, self.min, self.max))
