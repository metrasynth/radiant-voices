"""
Convenient access to classes that represent all SunVox module types.

Although the list below refers to the full Python module names that contain
each class, you can use a shorthand notation for easier access.

For example, to refer to the "Analog Generator" SunVox module, you
only need to refer to ``rv.modules.AnalogGenerator`` (instead of
``rv.modules.analoggenerator.AnalogGenerator``).
"""

MODULE_CLASSES = {}

# Must come first to avoid circular imports.
from rv.modules.module import Chunk, Module

from rv.modules.amplifier import Amplifier
from rv.modules.analoggenerator import AnalogGenerator
from rv.modules.compressor import Compressor
from rv.modules.dcblocker import DcBlocker
from rv.modules.delay import Delay
from rv.modules.distortion import Distortion
from rv.modules.drumsynth import DrumSynth
from rv.modules.echo import Echo
from rv.modules.eq import Eq
from rv.modules.feedback import Feedback
from rv.modules.filter import Filter
from rv.modules.filterpro import FilterPro
from rv.modules.flanger import Flanger
from rv.modules.fm import Fm
from rv.modules.generator import Generator
from rv.modules.glide import Glide
from rv.modules.gpio import Gpio
from rv.modules.input import Input
from rv.modules.kicker import Kicker
from rv.modules.lfo import Lfo
from rv.modules.loop import Loop
from rv.modules.metamodule import MetaModule
from rv.modules.modulator import Modulator
from rv.modules.multictl import MultiCtl
from rv.modules.multisynth import MultiSynth
from rv.modules.output import Output
from rv.modules.pitchshifter import PitchShifter
from rv.modules.reverb import Reverb
from rv.modules.sampler import Sampler
from rv.modules.sound2ctl import Sound2Ctl
from rv.modules.spectravoice import SpectraVoice
from rv.modules.vibrato import Vibrato
from rv.modules.vocalfilter import VocalFilter
from rv.modules.vorbisplayer import VorbisPlayer
from rv.modules.waveshaper import WaveShaper
