from __future__ import annotations

import io
import logging
from collections import defaultdict
from enum import Enum, IntEnum
from struct import pack
from typing import TYPE_CHECKING, Dict, List, Optional, Union

from logutils import BraceMessage as _F
from rv import ENCODING
from rv.cmidmap import ControllerMidiMap
from rv.controller import Controller, DependentRange
from rv.errors import RangeValidationError, raise_or_warn_controller_value_validation
from rv.modules.meta import ModuleMeta
from rv.option import Option
from rv.readers.reader import read_sunvox_file
from rv.synth import Synth

if TYPE_CHECKING:
    from rv.project import Project

log = logging.getLogger(__name__)


class Chunk:
    """A chunk of custom data related to a module."""

    __slots__ = ["chnm", "chdt", "chff", "chfr"]

    chnm: Optional[int]
    chdt: Optional[bytes]
    chff: int
    chfr: int

    def __init__(self):
        self.chnm = self.chdt = None
        self.chff = 0
        self.chfr = 44100

    def chunks(self):
        yield b"CHNM", pack("<I", self.chnm)
        yield b"CHDT", self.chdt
        if self.chff is not None:
            yield b"CHFF", pack("<I", self.chff)
        if self.chfr is not None:
            yield b"CHFR", pack("<I", self.chfr)


class ModuleList(list):
    """Ensures `>>` and `<<` work with lists."""

    def __init__(self, parent: Project, *args, **kwargs):
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
    """Different behaviors that"""  # [TODO] finish docstring

    receives_audio = 0x01
    receives_notes = 0x02
    receives_modulator = 0x03
    receives_feedback = 0x04

    sends_audio = 0x10
    sends_notes = 0x20
    sends_controls = 0x30
    sends_feedback = 0x40


class ModuleFlags(IntEnum):
    """
    All flags that can exist for a module's flags.

    Refer to lib_sunvox/psynth/psynth.h#L424 in SunVox library source code.
    """

    exists = 1 << 0  # 0x1
    output = 1 << 1  # 0x2
    generator = 1 << 3  # 0x8
    effect = 1 << 4  # 0x10
    initialized = 1 << 6  # 0x40
    mute = 1 << 7  # 0x80
    solo = 1 << 8  # 0x1_00
    get_speed_changes = 1 << 10  # 0x4_00
    hidden = 1 << 11  # 0x8_00
    no_fill_input = 1 << 13  # 0x20_00
    bypass = 1 << 14  # 0x40_00
    mute_solo_bypass = mute | solo | bypass  # 0x41_80
    use_mutex = 1 << 15  # 0x80_00
    ignore_mute = 1 << 16  # 0x1_00_00
    no_scope_buffer = 1 << 17  # 0x2_00_00
    output_is_empty = 1 << 18  # 0x4_00_00
    open = 1 << 19  # 0x8_00_00
    get_play_commands = 1 << 20  # 0x10_00_00
    get_render_setup_commands = 1 << 21  # 0x20_00_00
    feedback = 1 << 22  # 0x40_00_00
    get_stop_commands = 1 << 23  # 0x80_00_00
    no_render = 1 << 24  # 0x1_00_00_00
    selected = 1 << 25  # 0x2_00_00_00


class VisibleModuleFlags(IntEnum):
    """Flags that can be viewed and set by the user."""

    mute = 0x80
    solo = 0x100
    bypass = 0x4000
    selected = 0x02000000


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


class DisconnectingModule:
    def __init__(self, orig):
        self.__dict__["orig"] = orig

    def __getattr__(self, item):
        return getattr(self.__dict__["orig"], item)

    def __setattr__(self, key, value):
        return setattr(self.__dict__["orig"], key, value)

    def __invert__(self):
        return self.__dict__["orig"]


class Module(metaclass=ModuleMeta):
    """Abstract base class for all SunVox module classes.

    See `rv.modules.*` Python modules for subclasses that represent
    the actual SunVox module types.
    """

    name: str = ""
    mtype: str  # module type
    mgroup: str  # module group
    default_flags: int
    flags: int
    chnk: Union[int, bool] = False

    behaviors = set()

    controllers: Dict[str, Controller] = {}
    options: Dict[str, Option] = {}
    options_chnm = 0

    in_links: List[int]
    in_link_slots: List[int]
    out_links: List[int]
    out_link_slots: List[int]

    parent: Optional[Project]

    def __init__(self, **kw):
        self.index = kw.get("index")
        self.parent = kw.get("parent")
        self.controller_values = {}
        self.controllers_loaded = set()
        self.controller_midi_maps = defaultdict(ControllerMidiMap)
        for k, controller in self.controllers.items():
            if not isinstance(controller.value_type, DependentRange):
                v = kw.get(k, controller.default)
                controller.set_initial(self, v)
                self.controllers_loaded.add(k)
        for k, controller in self.controllers.items():
            if isinstance(controller.value_type, DependentRange):
                v = kw.get(k, controller.default)
                controller.set_initial(self, v)
                self.controllers_loaded.add(k)
        self.option_values = {}
        for k, option in self.options.items():
            v = kw.get(k, option.default)
            setattr(self, k, v)
        self.mod_finetune = kw.get("finetune", 0)
        self.mod_relative_note = kw.get("relative_note", 0)
        self.x = kw.get("x", 512)
        self.y = kw.get("y", 512)
        self.layer = kw.get("layer", 0)
        self.scale = kw.get("scale", 256)
        self.color = kw.get("color", (255, 255, 255))
        self.midi_in_always = kw.get("midi_in_always", False)
        self.midi_in_channel = kw.get("midi_in_channel", 0)
        self.midi_out_name = kw.get("midi_out_name")
        self.midi_out_channel = kw.get("midi_out_channel", 0)
        self.midi_out_bank = kw.get("midi_out_bank", -1)
        self.midi_out_program = kw.get("midi_out_program", -1)
        self.name = kw.get("name", self.name)
        self.visualization = kw.get("visualization", 0x000C0101)
        self.in_links = []
        self.in_link_slots = []
        self.out_links = []
        self.out_link_slots = []

    def __hash__(self):
        return hash((id(self.parent), self.index))

    def __repr__(self):
        attrs = [self.__class__.__name__]
        if self.index is not None:
            attrs.append(f"index={self.index}")
        if type(self) is not Module and self.name != self.mtype:
            attrs.append(f"name={self.name}")
        return f'<{" ".join(attrs)}>'

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

    def __invert__(self):
        return DisconnectingModule(self)

    def __int__(self):
        """Returns the module number needed to use the module in a pattern."""
        return self.index + 1

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
            raise_or_warn_controller_value_validation(
                e,
                log,
                "{:x}({}).{}={} is not within [{}, {}]".format(
                    self.index or 0, self.mtype, name, evalue, emin, emax
                ),
            )
            value = raw_value
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
        if type(self) is Module:
            raise RuntimeError("Cannot serialize base Module instance.")
        if in_project is None:
            in_project = self.parent is not None
        yield b"SFFF", pack("<I", self.flags)
        yield b"SNAM", self.name.encode(ENCODING)[:32].ljust(32, b"\0")
        if self.mtype is not None and self.mtype != "Output":
            yield b"STYP", self.mtype.encode(ENCODING) + b"\0"
        yield b"SFIN", pack("<i", self.mod_finetune)
        yield b"SREL", pack("<i", self.mod_relative_note)
        if in_project:
            yield b"SXXX", pack("<i", self.x)
            yield b"SYYY", pack("<i", self.y)
            yield b"SZZZ", pack("<i", self.layer)
        yield b"SSCL", pack("<I", self.scale)
        if in_project:
            yield b"SVPR", pack("<I", int(self.visualization))
        yield b"SCOL", pack("BBB", *self.color)
        yield (
            b"SMII",
            pack("<I", int(self.midi_in_always) + (self.midi_in_channel << 1)),
        )
        if self.midi_out_name:
            yield b"SMIN", self.midi_out_name.encode(ENCODING) + b"\0"
        yield b"SMIC", pack("<I", self.midi_out_channel)
        yield b"SMIB", pack("<i", self.midi_out_bank)
        yield b"SMIP", pack("<i", self.midi_out_program)

    def specialized_iff_chunks(self):
        """Yield specialized chunks needed for a module, if applicable.

        Override this in module subclasses as needed.
        """
        if self.options:
            yield from self.options_chunks()
        else:
            yield None, None

    def options_chunks(self):
        """Yield chunks necessary to save options for this module."""
        bytemap = [0] * 64
        bytes = 0
        for option in self.options.values():
            option_value = self.option_values.get(option.name)
            option_value &= (2**option.size) - 1
            option_value <<= option.bit
            bytemap[option.byte] |= option_value
            bytes = max(bytes, option.byte + 1)
        yield b"CHNM", pack("<I", self.options_chnm)
        yield b"CHDT", pack("B" * bytes, *bytemap[:bytes])

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

    def load_options(self, chunk: Chunk):
        bytemap = list(chunk.chdt)
        while len(bytemap) < 64:
            bytemap.append(0)
        for option in self.options.values():
            option_value = bytemap[option.byte]
            option_value >>= option.bit
            option_value &= (2**option.size) - 1
            if option.size == 1:
                option_value = bool(option_value)
            self.option_values[option.name] = option_value

    def finalize_load(self):
        pass
