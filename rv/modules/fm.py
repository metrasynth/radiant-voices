from enum import IntEnum

from rv.controller import Controller
from rv.modules import Module
from rv.modules import register


class Mode(IntEnum):

    HQ = 0
    HQ_MONO = 1
    LQ = 2
    LQ_MONO = 3


@register
class FmModule(Module):

    name = mtype = 'FM'

    c_volume = Controller((0, 256), 128)
    m_volume = Controller((0, 256), 48)
    panning = Controller((-128, 128), 0)
    c_freq_ratio = Controller((0, 16), 1)
    m_freq_ratio = Controller((0, 16), 1)
    m_feedback = Controller((0, 256), 0)
    c_attack = Controller((0, 512), 32)
    c_decay = Controller((0, 512), 32)
    c_sustain = Controller((0, 256), 128)
    c_release = Controller((0, 512), 64)
    m_attack = Controller((0, 512), 32)
    m_decay = Controller((0, 512), 32)
    m_sustain = Controller((0, 256), 128)
    m_release = Controller((0, 512), 64)
    m_scaling_per_key = Controller((0, 4), 0)
    polyphony_ch = Controller((1, 16), 4)
    mode = Controller(Mode, Mode.HQ)
