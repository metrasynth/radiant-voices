from collections import defaultdict

from rv.modules.module import Module
from rv.modules.unsupported import UnsupportedModule


MODULE_CLASSES = defaultdict(lambda: UnsupportedModule)


def register(cls):
    MODULE_CLASSES[cls.mtype] = cls
    return cls


from rv.modules import (
    amplifier,
    compressor,
    dcblocker,
    delay,
    distortion,
    drumsynth,
    echo,
    eq,
    feedback,
    filter,
    filterpro,
    flanger,
    fm,
    glide,
    gpio,
    input,
    kicker,
    lfo,
    loop,
    modulator,
    output,
    pitchshifter,
    reverb,
    vibrato,
    vocalfilter,
)
