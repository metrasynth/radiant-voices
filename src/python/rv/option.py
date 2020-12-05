from dataclasses import dataclass, field
from typing import List, Optional, Union


@dataclass
class Option:
    """Defines an option attached to a module.

    Options are typically booleans, although can sometimes be integers or enums.

    Options that have a `number` defined can be changed during playback as if they
    are controllers.
    """

    name: str
    byte: int  # index in byte map
    bit: int  # starting bit within the byte
    size: int  # in bits
    default: Union[int, bool]
    number: Optional[int] = None
    min: Optional[int] = None
    max: Optional[int] = None
    inverted: bool = False
    exclusive_of: List[str] = field(default_factory=list)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        value = instance.option_values[self.name]
        if self.inverted:
            return not value
        else:
            return value

    def __set__(self, instance, value):
        if None not in {self.min, self.max}:
            value = max(self.min, min(self.max, value))
        else:
            value = bool(value)
            if self.inverted:
                value = not value
        instance.option_values[self.name] = value
        callback = getattr(instance, "on_{}_changed".format(self.name), None)
        if callable(callback):
            callback(value)
        for other in self.exclusive_of:
            instance.option_values[other] = False
            callback = getattr(instance, "on_{}_changed".format(other), None)
            if callable(callback):
                callback(False)
