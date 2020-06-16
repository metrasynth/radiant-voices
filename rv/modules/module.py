import io
import logging
from collections import OrderedDict
from collections import defaultdict
from enum import Enum, IntEnum
from struct import pack
from typing import Dict

from logutils import BraceMessage as _F
from rv import ENCODING
from rv.cmidmap import ControllerMidiMap
from rv.controller import DependentRange, Controller
from rv.errors import ControllerValueError, RangeValidationError
from rv.modules.meta import ModuleMeta
from rv.readers.reader import read_sunvox_file
from rv.synth import Synth

log = logging.getLogger(__name__)


class Chunk:
    """A chunk of custom data related to a module."""

    __slots__ = ["chnm", "chdt", "chff", "chfr"]

    def __init__(self):
        self.chnm = self.chdt = None
        self.chff = 0
        self.chfr = 44100


class ModuleList(list):
    """Ensures `>>` and `<<` work with lists."""

    def __init__(self, parent, *args, **kwargs):
        super(ModuleList, self).__init__(*args, **kwargs)
        self.parent = parent

    def __lshift__(self, other):
        self.parent.connect(other, self)
        if isinstance(other, list):
            other = ModuleList(self.parent, other)
        return other

    def __rshift__(self, other):
        self.parent.connect(self, other)
        if isinstance(other, list):
            other = ModuleList(self.parent, other)
        return other


class Behavior(IntEnum):
    """Different behaviors that """

    receives_audio = 0x01
    receives_notes = 0x02
    receives_modulator = 0x03
    receives_feedback = 0x04

    sends_audio = 0x10
    sends_notes = 0x20
    sends_controls = 0x30
    sends_feedback = 0x40


class ModuleFlags(IntEnum):
    """All flags that can exist for a module's flags."""

    exists = 0x1
    output = 0x2
    generator = 0x8
    effect = 0x10
    initialized = 0x40
    mute = 0x80
    solo = 0x100
    get_speed_changes = 0x400
    hidden = 0x800
    multi = 0x1000
    no_fill_input = 0x2000
    bypass = 0x4000
    use_mutex = 0x8000
    ignore_mute = 0x10000
    no_scope_buffer = 0x20000
    output_is_empty = 0x40000
    open = 0x80000
    get_play_commands = 0x100000
    get_render_setup_commands = 0x200000
    feedback = 0x400000
    get_stop_commands = 0x800000


class VisibleModuleFlags(IntEnum):
    """Flags that can be viewed and set by the user."""

    mute = 0x80
    solo = 0x100
    bypass = 0x4000


class LevelMode(IntEnum):

    off = 0
    mono = 1
    stereo = 2
    color = 3
    glow = 4


class Orientation(IntEnum):

    horizontal = 0
    vertical = 1


class OscilloscopeMode(IntEnum):

    off = 0
    points = 1
    lines = 2
    bars = 3
    bars_2 = 4
    phase_1 = 5
    phase_2 = 6
    xy = 7


class Visualization:
    def __init__(self, value):
        self.value = value

    def __int__(self):
        return self.value

    @property
    def level_mode(self):
        return LevelMode(self.value & 0b11111)

    @level_mode.setter
    def level_mode(self, v):
        self.value = self.value - self.level_mode + (v & 0b11111)

    @property
    def orientation(self):
        return Orientation(self.value >> 5 & 1)

    @orientation.setter
    def orientation(self, v):
        self.value = self.value - (int(self.orientation) << 5) + ((int(v) & 1) << 5)

    @property
    def oscilloscope_mode(self):
        return OscilloscopeMode(self.value >> 8 & 0b11111)

    @oscilloscope_mode.setter
    def oscilloscope_mode(self, v):
        self.value = (
            self.value - (int(self.oscilloscope_mode) << 8) + ((int(v) & 0b11111) << 8)
        )

    @property
    def oscilloscope_size(self):
        return self.value >> 16 & 0xFF

    @oscilloscope_size.setter
    def oscilloscope_size(self, v):
        self.value = (
            self.value - (self.oscilloscope_size << 16) + (max(0, min(v, 0xFF)) << 16)
        )

    @property
    def bg_transparency(self):
        return self.value >> 24 & 3

    @bg_transparency.setter
    def bg_transparency(self, v):
        self.value = (
            self.value - (self.bg_transparency << 24) + (max(0, min(v, 3)) << 24)
        )

    @property
    def shadow_opacity(self):
        return self.value >> 26 & 3

    @shadow_opacity.setter
    def shadow_opacity(self, v):
        self.value = (
            self.value - (self.shadow_opacity << 26) + (max(0, min(v, 3)) << 26)
        )


class Module(metaclass=ModuleMeta):
    """Abstract base class for all SunVox module classes.

    See `rv.modules.*` Python modules for subclasses that represent
    the actual SunVox module types.
    """

    name = None
    mtype = None  # module type
    mgroup = None  # module group
    flags = None
    chnk = False

    behaviors = set()

    controllers: Dict[str, Controller] = OrderedDict()
    options = OrderedDict()
    options_chnm = 0

    def __init__(self, **kw):
        self.index = kw.get("index", None)
        self.parent = kw.get("parent", None)
        self.controller_values = OrderedDict()
        self.controllers_loaded = set()
        self.controller_midi_maps = defaultdict(ControllerMidiMap)
        for k, controller in self.controllers.items():
            if not isinstance(controller.value_type, DependentRange):
                v = kw.get(k) if k in kw else controller.default
                controller.set_initial(self, v)
                self.controllers_loaded.add(k)
        for k, controller in self.controllers.items():
            if isinstance(controller.value_type, DependentRange):
                v = kw.get(k) if k in kw else controller.default
                controller.set_initial(self, v)
                self.controllers_loaded.add(k)
        self.option_values = OrderedDict()
        for k, option in self.options.items():
            v = kw.get(k) if k in kw else option.default
            setattr(self, k, v)
        self.finetune = kw.get("finetune", 0)
        self.relative_note = kw.get("relative_note", 0)
        self.x = kw.get("x", 512)
        self.y = kw.get("y", 512)
        self.layer = kw.get("layer", 0)
        self.scale = kw.get("scale", 256)
        self.color = kw.get("color", (255, 255, 255))
        self.midi_in_always = kw.get("midi_in_always", False)
        self.midi_in_channel = kw.get("midi_in_channel", 0)
        self.midi_out_name = kw.get("midi_out_name", None)
        self.midi_out_channel = kw.get("midi_out_channel", 0)
        self.midi_out_bank = kw.get("midi_out_bank", -1)
        self.midi_out_program = kw.get("midi_out_program", -1)
        self.name = kw.get("name", self.name)
        self.visualization = kw.get("visualization", 0x000C0101)
        self.incoming_links = []

    def __repr__(self):
        attrs = [self.__class__.__name__]
        if self.index is not None:
            attrs.append("index={}".format(self.index))
        if self.name != self.mtype:
            attrs.append("name={}".format(self.name))
        return "<{}>".format(" ".join(attrs))

    def __lshift__(self, other):
        self.parent.connect(other, self)
        if isinstance(other, list):
            other = ModuleList(self.parent, other)
        return other

    def __rshift__(self, other):
        self.parent.connect(self, other)
        if isinstance(other, list):
            other = ModuleList(self.parent, other)
        return other

    @property
    def visualization(self):
        return Visualization(self._visualization)

    @visualization.setter
    def visualization(self, v):
        self._visualization = v

    def clone(self):
        synth = Synth(self)
        f = io.BytesIO()
        synth.write_to(f)
        f.seek(0)
        synth2 = read_sunvox_file(f)
        f.close()
        return synth2.module

    def get_raw(self, name):
        """Return the raw (unsigned) value for the named controller."""
        controller = self.controllers[name]
        t = controller.instance_value_type(self)
        value = getattr(self, name)
        to_raw_value = getattr(t, "to_raw_value", int)
        if isinstance(value, Enum):
            value = value.value
        return to_raw_value(0 if value is None else value)

    def set_raw(self, name, raw_value):
        """Set the value for the named controller based on given raw value."""
        controller = self.controllers[name].controller(self)
        t = controller.instance_value_type(self)
        from_raw_value = getattr(t, "from_raw_value", int)
        try:
            value = t(from_raw_value(raw_value))
        except RangeValidationError as e:
            evalue, emin, emax = e.args
            raise ControllerValueError(
                "{:x}({}).{}={} is not within [{}, {}]".format(
                    self.index or 0, self.mtype, name, evalue, emin, emax
                )
            )
        self.controller_values[name] = value

    def propagate_down(self, controller_name, value):
        controller = self.controllers[controller_name]
        controller.propagate_down(self, value)

    def on_controller_changed(self, controller, value, down, up):
        if up and self.parent:
            self.parent.on_controller_changed(
                self, controller, value, down=False, up=True
            )

    def iff_chunks(self, in_project=None):
        """Yield all standard chunks needed for a module."""
        if in_project is None:
            in_project = self.parent is not None
        yield (b"SFFF", pack("<I", self.flags))
        yield (b"SNAM", self.name.encode(ENCODING)[:32].ljust(32, b"\0"))
        if self.mtype is not None and self.mtype != "Output":
            yield (b"STYP", self.mtype.encode(ENCODING) + b"\0")
        yield (b"SFIN", pack("<i", self.finetune))
        yield (b"SREL", pack("<i", self.relative_note))
        if in_project:
            yield (b"SXXX", pack("<i", self.x))
            yield (b"SYYY", pack("<i", self.y))
            yield (b"SZZZ", pack("<i", self.layer))
        yield (b"SSCL", pack("<I", self.scale))
        if in_project:
            yield (b"SVPR", pack("<I", int(self.visualization)))
        yield (b"SCOL", pack("BBB", *self.color))
        yield (
            b"SMII",
            pack("<I", int(self.midi_in_always) + (self.midi_in_channel << 1)),
        )
        if self.midi_out_name:
            yield (b"SMIN", self.midi_out_name.encode(ENCODING) + b"\0")
        yield (b"SMIC", pack("<I", self.midi_out_channel))
        yield (b"SMIB", pack("<i", self.midi_out_bank))
        yield (b"SMIP", pack("<i", self.midi_out_program))

    def specialized_iff_chunks(self):
        """Yield specialized chunks needed for a module, if applicable.

        Override this in module subclasses as needed.
        """
        if self.options:
            yield from self.options_chunks()
        else:
            yield (None, None)

    def options_chunks(self):
        """Yield chunks necessary to save options for this module."""
        yield (b"CHNM", pack("<I", self.options_chnm))
        values = list(self.option_values.values())
        values += [False] * (64 - len(values))
        yield (b"CHDT", pack("B" * 64, *values))

    def load_chunk(self, chunk):
        """Load a CHNK/CHNM/CHDT/CHFF/CHFR block into this module."""
        log.warning(_F("load_chunk not implemented for {}", self.__class__.__name__))

    def load_cmid(self, data):
        names = self.controllers.keys()
        for i, name in enumerate(names):
            offset = i * 8
            cmid_data = data[offset : offset + 8]
            if len(cmid_data) == 8:
                self.controller_midi_maps[name].cmid_data = cmid_data

    def load_options(self, chunk):
        for i, name in enumerate(self.options.keys()):
            value = 0 if i >= len(chunk.chdt) else chunk.chdt[i]
            self.option_values[name] = value

    def finalize_load(self):
        pass
