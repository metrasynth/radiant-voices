from io import BytesIO
from itertools import chain
from struct import pack

import rv
from rv.chunks import ArrayChunk
from rv.controller import Controller
from rv.modules import Module
from rv.option import Option
from rv.project import Project


MAX_USER_DEFINED_CONTROLLERS = 27


class UserDefined(Controller):
    label = None

    def __init__(self):
        super().__init__(None, None, detached=True)


class MetaModule(Module):
    """
    In addition to standard controllers, you can assign zero or more
    user-defined controllers which map to module/controller pairs
    in the project embedded within the MetaModule.
    """

    name = mtype = 'MetaModule'
    mgroup = 'Misc'
    chnk = 0x10
    options_chnm = 0x02

    class Mapping(object):
        def __init__(self, value):
            self.module, self.controller = value[0], value[1] + 1

    class MappingArray(ArrayChunk):
        chnm = 1
        length = 32
        type = 'HH'
        element_size = 2 * 2
        @property
        def default(self):
            return [MetaModule.Mapping((0, 0)) for x in range(self.length)]
        @property
        def encoded_values(self):
            return list(chain.from_iterable(
                (x.module, x.controller - 1) for x in self.values))
        @property
        def python_type(self):
            return MetaModule.Mapping
        def update_user_defined_controllers(self, metamodule):
            project = metamodule.project
            items = zip(metamodule.mappings.values, metamodule.user_defined)
            for mapping, user_defined_controller in items:
                if mapping.module == 0:
                    continue
                mod = project.modules[mapping.module]
                controller_index = mapping.controller - 1
                controller = list(mod.controllers.values())[controller_index]
                user_defined_controller.value_type = controller.value_type
                user_defined_controller.default = controller.default
                metamodule.controller_values[user_defined_controller.name] = \
                    mod.controller_values[controller.name]

    volume = Controller((0, 1024), 256)
    input_module = Controller((1, 256), 1)
    play_patterns = Controller(bool, False)
    bpm = Controller((1, 800), 125)     # TODO: propagate to project and back
    tpl = Controller((1, 31), 6)        # TODO: propagate to project and back

    # TODO: propagate changes in bpm/tpl to subproject and back

    user_defined = [UserDefined() for x in range(MAX_USER_DEFINED_CONTROLLERS)]
    (user_defined_1, user_defined_2, user_defined_3, user_defined_4,
     user_defined_5, user_defined_6, user_defined_7, user_defined_8,
     user_defined_9, user_defined_10, user_defined_11, user_defined_12,
     user_defined_13, user_defined_14, user_defined_15, user_defined_16,
     user_defined_17, user_defined_18, user_defined_19, user_defined_20,
     user_defined_21, user_defined_22, user_defined_23, user_defined_24,
     user_defined_25, user_defined_26, user_defined_27) = user_defined

    user_defined_controllers = Option(0, (0, MAX_USER_DEFINED_CONTROLLERS))
    arpeggiator = Option(False)
    apply_velocity_to_project = Option(False)

    def __init__(self, **kwargs):
        project = kwargs.get('project', None)
        super(MetaModule, self).__init__(**kwargs)
        self.mappings = self.MappingArray()
        self.project = project if project else Project()
        self.project.metamodule = self

    def on_controller_changed(self, controller, value, down, up):
        if isinstance(controller, UserDefined) and down:
            mapping_index = controller.number - self.user_defined[0].number
            mapping = self.mappings.values[mapping_index]
            module = self.project.modules[mapping.module]
            controller_index = mapping.controller - 1
            controller = list(module.controllers.values())[controller_index]
            controller.propagate(module, value, down=True)
        super(MetaModule, self).on_controller_changed(
            controller, value, down, up)

    def on_embedded_controller_changed(self, module, controller, value):
        for i, mapping in enumerate(self.mappings.values):
            module_matches = mapping.module == module.index
            controller_matches = mapping.controller == controller.number
            if module_matches and controller_matches:
                name = self.user_defined[i].name
                setattr(self, name, value)

    def on_user_defined_controllers_changed(self, value):
        detached_values = (
            [False] * value +
            [True] * (MAX_USER_DEFINED_CONTROLLERS - value)
        )
        for controller, detached in zip(self.user_defined, detached_values):
            controller.detached = detached

    def update_user_defined_controllers(self):
        self.mappings.update_user_defined_controllers(self)

    def specialized_iff_chunks(self):
        yield (b'CHNM', pack('<I', 0))
        yield (b'CHDT', self.project.read())
        yield (b'CHFF', pack('<I', 0))
        yield (b'CHFR', pack('<I', 0))
        for chunk in self.mappings.chunks():
            yield chunk
        for i, controller in enumerate(self.user_defined, 8):
            if not controller.detached and controller.label is not None:
                yield (b'CHNM', pack('<I', i))
                yield (b'CHDT', controller.label.encode(rv.ENCODING) + b'\0')
                yield (b'CHFF', pack('<I', 0))
                yield (b'CHFR', pack('<I', 0))

    def load_chunk(self, chunk):
        if chunk.chnm == self.options_chnm:
            self.load_options(chunk)
        elif chunk.chnm == 0:
            self.load_project(chunk)
        elif chunk.chnm == 1:
            self.mappings.bytes = chunk.chdt
        elif chunk.chnm >= 8:
            self.load_label(chunk)

    def load_project(self, chunk):
        self.project = rv.read_sunvox_file(BytesIO(chunk.chdt))

    def load_label(self, chunk):
        controller = self.user_defined[chunk.chnm - 8]
        data = chunk.chdt
        data = data[:data.find(0)] if 0 in data else data
        controller.label = data.decode(rv.ENCODING)
