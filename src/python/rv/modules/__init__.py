"""
Convenient access to classes that represent all SunVox module types.

Although the list below refers to the full Python module names that contain
each class, you can use a shorthand notation for easier access.

For example, to refer to the "Analog Generator" SunVox module, you
only need to refer to ``rv.modules.AnalogGenerator`` (instead of
``rv.modules.analoggenerator.AnalogGenerator``).
"""

# isort:skip_file
# flake8: noqa

MODULE_CLASSES = {}

# Must come first to avoid circular imports.
from .module import (
    Behavior,
    Chunk,
    LevelMode,
    Module,
    ModuleFlags,
    Orientation,
    OscilloscopeMode,
    VisibleModuleFlags,
)

from .adsr import Adsr
from .amplifier import Amplifier
from .analoggenerator import AnalogGenerator
from .compressor import Compressor
from .ctl2note import Ctl2Note
from .dcblocker import DcBlocker
from .delay import Delay
from .distortion import Distortion
from .drumsynth import DrumSynth
from .echo import Echo
from .eq import Eq
from .feedback import Feedback
from .filter import Filter
from .filterpro import FilterPro
from .flanger import Flanger
from .fm import Fm
from .generator import Generator
from .glide import Glide
from .gpio import Gpio
from .input import Input
from .kicker import Kicker
from .lfo import Lfo
from .loop import Loop
from .metamodule import MetaModule
from .modulator import Modulator
from .multictl import MultiCtl
from .multisynth import MultiSynth
from .output import Output
from .pitch2ctl import Pitch2Ctl
from .pitchdetector import PitchDetector
from .pitchshifter import PitchShifter
from .reverb import Reverb
from .sampler import Sampler
from .sound2ctl import Sound2Ctl
from .spectravoice import SpectraVoice
from .velocity2ctl import Velocity2Ctl
from .vibrato import Vibrato
from .vocalfilter import VocalFilter
from .vorbisplayer import VorbisPlayer
from .waveshaper import WaveShaper

__all__ = [
    "Adsr",
    "Amplifier",
    "AnalogGenerator",
    "Behavior",
    "Chunk",
    "Compressor",
    "Ctl2Note",
    "DcBlocker",
    "Delay",
    "Distortion",
    "DrumSynth",
    "Echo",
    "Eq",
    "Feedback",
    "Filter",
    "FilterPro",
    "Flanger",
    "Fm",
    "Generator",
    "Glide",
    "Gpio",
    "Input",
    "Kicker",
    "LevelMode",
    "Lfo",
    "Loop",
    "MetaModule",
    "Modulator",
    "Module",
    "ModuleFlags",
    "MultiCtl",
    "MultiSynth",
    "Orientation",
    "OscilloscopeMode",
    "Output",
    "Pitch2Ctl",
    "PitchDetector",
    "PitchShifter",
    "Reverb",
    "Sampler",
    "Sound2Ctl",
    "SpectraVoice",
    "Velocity2Ctl",
    "Vibrato",
    "VisibleModuleFlags",
    "VocalFilter",
    "VorbisPlayer",
    "WaveShaper",
]
