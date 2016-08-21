from collections import OrderedDict
from struct import pack

from rv import ENCODING
from rv.modules.meta import ModuleMeta


class Module(object, metaclass=ModuleMeta):
    """Abstract base class for all SunVox module classes.

    See `rv.modules.*` Python modules for subclasses that represent
    the actual SunVox module types.
    """

    name = None
    mtype = None  # module type
    flags = 0x00000049

    controllers = OrderedDict()

    def __init__(self, **kw):
        self.index = None
        self.controller_values = OrderedDict()
        for k, controller in self.controllers.items():
            v = kw.get(k) if k in kw else controller.default
            setattr(self, k, v)
        self.finetune = 0
        self.relative_note = 0
        self.x_position = 512
        self.y_position = 512
        self.layer = 0
        self.scale = 256
        self.color = (255, 255, 255)
        self.midi_out_channel = 0
        self.midi_out_bank = -1
        self.midi_out_program = -1
        self.visualization = 0x000c0101
        self.incoming_links = []

    def get_raw(self, name):
        """Return the raw (unsigned) value for the named controller."""
        controller = self.controllers[name]
        value_type = controller.value_type
        value = getattr(self, name)
        to_raw_value = getattr(value_type, 'to_raw_value', int)
        raw_value = to_raw_value(value)
        return raw_value

    def set_raw(self, name, raw_value):
        """Set the value for the named controller based on given raw value."""
        controller = self.controllers[name]
        value_type = controller.value_type
        value = value_type(raw_value)
        setattr(self, name, value)

    def chunks(self):
        """Yield all chunks needed for a module."""
        yield (b'SFFF', pack('<I', self.flags))
        yield (b'SNAM', self.name.encode(ENCODING)[:32].ljust(32, b'\0'))
        if self.mtype is not None:
            yield (b'STYP', self.mtype.encode(ENCODING) + b'\0')
        yield (b'SFIN', pack('<i', self.finetune))
        yield (b'SREL', pack('<i', self.relative_note))
        yield (b'SXXX', pack('<i', self.x_position))
        yield (b'SYYY', pack('<i', self.y_position))
        yield (b'SZZZ', pack('<i', self.layer))
        yield (b'SSCL', pack('<I', self.scale))
        yield (b'SVPR', b'\x01\x01\x0c\x00')  # ?
        yield (b'SCOL', pack('BBB', *self.color))
        yield (b'SMIC', pack('<i', self.midi_out_channel))
        yield (b'SMIB', pack('<i', self.midi_out_bank))
        yield (b'SMIP', pack('<i', self.midi_out_program))
        for chunk in self.specialized_chunks():
            yield chunk

    def specialized_chunks(self):
        """Yield specialized chunks needed for a module, if applicable.

        Override this in module subclasses as needed.
        """
        yield (None, None)
