import re
from io import BytesIO
from itertools import chain
from string import digits
from struct import pack

import rv
from rv.chunks import ArrayChunk
from rv.controller import Controller, Range
from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.metamodule import BaseMetaModule
from rv.project import Project
from rv.readers.reader import read_sunvox_file
from slugify import slugify as _slugify

MAX_USER_DEFINED_CONTROLLERS = 96
USER_DEFINED_RE = re.compile(r"user_defined_\d+")


def slugify(s):
    s = _slugify(s, separator="_", lowercase=True)
    if s == "":
        return "_"
    if s[0] in digits:
        s = f"_{s}"
    return s


class UserDefined(Controller):
    label = None

    def __init__(self, number):
        self.name = f"user_defined_{number + 1}"
        self.number = number + 6
        super().__init__((0, 44100), 0, attached=False)

    def attach(self, instance):
        self._attached = True

    def detach(self, instance):
        self._attached = False


class UserDefinedProxy(Controller):
    def __init__(self, index):
        self.index = index
        super(UserDefinedProxy, self).__init__((0, 32768), 0)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        ctl = instance.user_defined[self.index]
        return ctl.__get__(instance, owner)

    def __set__(self, instance, value):
        if instance is not None:
            ctl = instance.user_defined[self.index]
            return ctl.__set__(instance, value)

    def controller(self, instance):
        return instance.user_defined[self.index]

    def attached(self, instance):
        return self.controller(instance).attached(instance)

    def attach(self, instance):
        return self.controller(instance).attach(instance)

    def detach(self, instance):
        return self.controller(instance).detach(instance)

    def instance_value_type(self, instance):
        return self.controller(instance).value_type


class MetaModule(BaseMetaModule, Module):
    """
    In addition to standard controllers, you can assign zero or more
    user-defined controllers which map to module/controller pairs
    in the project embedded within the MetaModule.
    """

    options_chnm = 0x02

    behaviors = {B.receives_audio, B.receives_notes, B.sends_audio, B.sends_notes}

    class Mapping:
        def __init__(self, value):
            self.module, self.controller = value[0], value[1]

    class MappingArray(ArrayChunk):
        chnm = 1
        length = MAX_USER_DEFINED_CONTROLLERS
        type = "HH"
        element_size = 2 * 2

        def default(self, _):
            return MetaModule.Mapping((0, 0))

        def _set_bytes(self, value):
            super(MetaModule.MappingArray, self)._set_bytes(value)

            while len(self.values) < self.length:
                self.values.append(MetaModule.Mapping((0, 0)))

        @property
        def encoded_values(self):
            return list(
                chain.from_iterable((x.module, x.controller) for x in self.values)
            )

        @property
        def python_type(self):
            return MetaModule.Mapping

        @staticmethod
        def update_user_defined_controllers(metamodule):
            project = metamodule.project
            items = zip(metamodule.mappings.values, metamodule.user_defined)
            for idx, (mapping, user_defined_controller) in enumerate(items):
                if idx == metamodule.user_defined_controllers:
                    break
                if mapping.module == 0 or mapping.module >= len(project.modules):
                    continue
                mod = project.modules[mapping.module]
                if not mod:
                    continue
                controller_index = mapping.controller
                controller_values = list(mod.controllers.values())
                if controller_index >= len(controller_values):
                    continue
                controller = controller_values[controller_index]
                user_defined_controller.value_type = controller.instance_value_type(mod)
                user_defined_controller.default = controller.default
                metamodule.controller_values[user_defined_controller.name] = (
                    mod.controller_values[controller.name]
                )

    (
        user_defined_1,
        user_defined_2,
        user_defined_3,
        user_defined_4,
        user_defined_5,
        user_defined_6,
        user_defined_7,
        user_defined_8,
        user_defined_9,
        user_defined_10,
        user_defined_11,
        user_defined_12,
        user_defined_13,
        user_defined_14,
        user_defined_15,
        user_defined_16,
        user_defined_17,
        user_defined_18,
        user_defined_19,
        user_defined_20,
        user_defined_21,
        user_defined_22,
        user_defined_23,
        user_defined_24,
        user_defined_25,
        user_defined_26,
        user_defined_27,
        user_defined_28,
        user_defined_29,
        user_defined_30,
        user_defined_31,
        user_defined_32,
        user_defined_33,
        user_defined_34,
        user_defined_35,
        user_defined_36,
        user_defined_37,
        user_defined_38,
        user_defined_39,
        user_defined_40,
        user_defined_41,
        user_defined_42,
        user_defined_43,
        user_defined_44,
        user_defined_45,
        user_defined_46,
        user_defined_47,
        user_defined_48,
        user_defined_49,
        user_defined_50,
        user_defined_51,
        user_defined_52,
        user_defined_53,
        user_defined_54,
        user_defined_55,
        user_defined_56,
        user_defined_57,
        user_defined_58,
        user_defined_59,
        user_defined_60,
        user_defined_61,
        user_defined_62,
        user_defined_63,
        user_defined_64,
        user_defined_65,
        user_defined_66,
        user_defined_67,
        user_defined_68,
        user_defined_69,
        user_defined_70,
        user_defined_71,
        user_defined_72,
        user_defined_73,
        user_defined_74,
        user_defined_75,
        user_defined_76,
        user_defined_77,
        user_defined_78,
        user_defined_79,
        user_defined_80,
        user_defined_81,
        user_defined_82,
        user_defined_83,
        user_defined_84,
        user_defined_85,
        user_defined_86,
        user_defined_87,
        user_defined_88,
        user_defined_89,
        user_defined_90,
        user_defined_91,
        user_defined_92,
        user_defined_93,
        user_defined_94,
        user_defined_95,
        user_defined_96,
    ) = [UserDefinedProxy(__i) for __i in range(MAX_USER_DEFINED_CONTROLLERS)]

    def __init__(self, **kwargs):
        project = kwargs.get("project")
        self.user_defined = [
            UserDefined(i) for i in range(MAX_USER_DEFINED_CONTROLLERS)
        ]
        super(MetaModule, self).__init__(**kwargs)
        self.mappings = self.MappingArray()
        self.project = project or Project()
        self.project.metamodule = self

    def __getattr__(self, key):
        if USER_DEFINED_RE.match(key):
            ctl = self.controllers[key]
            return ctl.__get__(self, None)
        else:
            if "user_defined" in self.__dict__:
                try:
                    i = self.user_defined_aliases.index(key)
                except ValueError:
                    raise AttributeError()
                else:
                    ctl_name = list(self.controllers)[i + 5]
                    ctl = self.controllers[ctl_name]
                    return ctl.__get__(self, None)
            else:
                raise AttributeError()

    def __setattr__(self, key, value):
        if USER_DEFINED_RE.match(key):
            ctl = self.controllers[key]
            return ctl.__set__(self, value)
        else:
            try:
                i = self.user_defined_aliases.index(key)
            except ValueError:
                super().__setattr__(key, value)
            else:
                ctl_name = list(self.controllers)[i + 5]
                ctl = self.controllers[ctl_name]
                return ctl.__set__(self, value)

    def __dir__(self):
        return list(super().__dir__()) + [
            name for name in self.user_defined_aliases if name
        ]

    @property
    def chnk(self):
        return 8 + MAX_USER_DEFINED_CONTROLLERS

    @property
    def user_defined_aliases(self):
        return (
            [
                f"u_{slugify(ctl.label).lower()}" if ctl.label else None
                for ctl in self.user_defined
                if ctl.attached(self)
            ]
            if hasattr(self, "user_defined")
            else []
        )

    def on_controller_changed(self, controller, value, down, up):
        if isinstance(controller, UserDefined) and down:
            mapping_index = controller.number - self.user_defined[0].number
            mapping = self.mappings.values[mapping_index]
            mod = self.project.modules[mapping.module]
            controller_index = mapping.controller
            controllers = list(mod.controllers.items())
            ctl_name, ctl = controllers[controller_index]
            t = ctl.instance_value_type(mod)
            if isinstance(t, Range):
                value += t.min
            ctl.propagate(mod, value, down=True)
        super(MetaModule, self).on_controller_changed(controller, value, down, up)

    def on_embedded_controller_changed(self, module, controller, value):
        for i, mapping in enumerate(self.mappings.values):
            module_matches = mapping.module == module.index
            controller_matches = mapping.controller == controller.number
            if module_matches and controller_matches:
                name = self.user_defined[i].name
                setattr(self, name, value)

    def on_user_defined_controllers_changed(self, value):
        self.recompute_controller_attachment()

    def recompute_controller_attachment(self):
        ctl_count = self.user_defined_controllers
        attached_values = [True] * ctl_count + [False] * (
            MAX_USER_DEFINED_CONTROLLERS - ctl_count
        )
        for controller, attached in zip(self.user_defined, attached_values):
            if attached:
                controller.attach(self)
            else:
                controller.detach(self)

    def update_user_defined_controllers(self):
        self.mappings.update_user_defined_controllers(self)

    def specialized_iff_chunks(self):
        yield b"CHNM", pack("<I", 0)
        yield b"CHDT", self.project.read()
        yield from self.mappings.chunks()
        yield from super(MetaModule, self).specialized_iff_chunks()
        for i, controller in enumerate(self.user_defined, 8):
            if controller.attached(self) and controller.label is not None:
                yield b"CHNM", pack("<I", i)
                yield b"CHDT", controller.label.encode(rv.ENCODING) + b"\0"

    def load_chunk(self, chunk):
        if chunk.chnm == self.options_chnm:
            self.load_options(chunk)
        elif chunk.chnm == 0:
            self.load_project(chunk)
        elif chunk.chnm == 1:
            # self.mappings.length = len(chunk.chdt) // self.mappings.element_size
            self.mappings.reset()
            self.mappings.bytes = chunk.chdt
        elif chunk.chnm >= 8:
            self.load_label(chunk)

    def load_project(self, chunk):
        self.project = read_sunvox_file(BytesIO(chunk.chdt))

    def load_label(self, chunk):
        controller = self.user_defined[chunk.chnm - 8]
        data = chunk.chdt
        data = data[: data.find(0)] if 0 in data else data
        controller.label = data.decode(rv.ENCODING)
