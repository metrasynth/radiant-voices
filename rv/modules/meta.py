from collections import OrderedDict
from textwrap import dedent

from rv.controller import Controller
from rv.modules import MODULE_CLASSES


class ModuleMeta(type):
    """Ensures controllers are set up in the order they are defined."""

    def __init__(cls, class_name, bases, class_dict):
        type.__init__(cls, class_name, bases, class_dict)
        ordered_controllers = [(k, v) for k, v in class_dict.items()
                               if isinstance(v, Controller)]
        ordered_controllers.sort(key=lambda x: x[1]._order)
        cls.controllers = OrderedDict()
        for i, (k, v) in enumerate(ordered_controllers, 1):
            v.label = k.replace('_', ' ').title()
            v.name = k
            v.number = i
            cls.controllers[k] = v
        if class_dict.get('mtype') is not None:
            MODULE_CLASSES[class_dict['mtype']] = cls
        cls.__doc__ = dedent("""\
            "{mtype}" SunVox {mgroup} Module
        """).format(**class_dict)
