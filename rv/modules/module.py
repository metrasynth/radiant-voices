import logging
from enum import Enum

from logutils import BraceMessage as _F
log = logging.getLogger(__name__)

from collections import OrderedDict
from struct import pack, unpack

from rv import ENCODING
from rv.modules.meta import ModuleMeta


class Chunk(object):
    """A chunk of custom data related to a module."""

    __slots__ = ['chnm', 'chdt', 'chff', 'chfr']

    def __init__(self):
        self.chnm = self.chdt = self.chff = self.chfr = None


class Module(object, metaclass=ModuleMeta):
    """Abstract base class for all SunVox module classes.

    See `rv.modules.*` Python modules for subclasses that represent
    the actual SunVox module types.
    """

    name = None
    mtype = None  # module type
    mgroup = None  # module group
    flags = 0x00000049
    chnk = None

    controllers = OrderedDict()
    options = OrderedDict()
    options_chnm = 0

    def __init__(self, **kw):
        self.index = None
        self.parent = kw.get('parent', None)
        self.controller_values = OrderedDict()
        for k, controller in self.controllers.items():
            v = kw.get(k) if k in kw else controller.default
            controller.set_initial(self, v)
        self.option_values = OrderedDict()
        for k, option in self.options.items():
            v = kw.get(k) if k in kw else option.default
            setattr(self, k, v)
        self.finetune = kw.get('finetune', 0)
        self.relative_note = kw.get('relative_note', 0)
        self.x_position = kw.get('x_position', 512)
        self.y_position = kw.get('y_position', 512)
        self.layer = kw.get('layer', 0)
        self.scale = kw.get('scale', 256)
        self.color = kw.get('color', (255, 255, 255))
        self.midi_out_channel = kw.get('midi_out_channel', 0)
        self.midi_out_bank = kw.get('midi_out_bank', -1)
        self.midi_out_program = kw.get('midi_out_program', -1)
        self.visualization = kw.get('visualization', 0x000c0101)
        self.incoming_links = []

    def get_raw(self, name):
        """Return the raw (unsigned) value for the named controller."""
        controller = self.controllers[name]
        value_type = controller.value_type
        value = getattr(self, name)
        to_raw_value = getattr(value_type, 'to_raw_value', int)
        if isinstance(value, Enum):
            value = value.value
        raw_value = to_raw_value(0 if value is None else value)
        return raw_value

    def set_raw(self, name, raw_value):
        """Set the value for the named controller based on given raw value."""
        controller = self.controllers[name]
        value_type = controller.value_type
        from_raw_value = getattr(value_type, 'from_raw_value', int)
        value = value_type(from_raw_value(raw_value))
        setattr(self, name, value)

    def propagate_down(self, controller_name, value):
        controller = self.controllers[controller_name]
        controller.propagate_down(self, value)

    def on_controller_changed(self, controller, value, down, up):
        if up and self.parent:
            self.parent.on_controller_changed(
                self, controller, value, down=False, up=True)

    def iff_chunks(self):
        """Yield all standard chunks needed for a module."""
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

    def specialized_iff_chunks(self):
        """Yield specialized chunks needed for a module, if applicable.

        Override this in module subclasses as needed.
        """
        yield (None, None)

    def options_chunks(self):
        """Yield chunks necessary to save options for this module."""
        yield (b'CHNM', pack('<I', self.options_chnm))
        values = list(self.option_values.values())
        values += [False] * (64 - len(values))
        yield (b'CHDT', pack('B' * 64, *values))
        yield (b'CHFF', pack('<I', 0))
        yield (b'CHFR', pack('<I', 0))

    def load_chunk(self, chunk):
        """Load a CHNK/CHNM/CHDT/CHFF/CHFR block into this module."""
        log.warn(_F('load_chunk not implemented for {}',
                    self.__class__.__name__))

    def load_options(self, chunk):
        for i, name in enumerate(self.options.keys()):
            value = chunk.chdt[i]
            setattr(self, name, value)
