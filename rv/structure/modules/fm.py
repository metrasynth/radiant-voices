from rv.structure.controller import Controller, Range
from rv.structure.module import GenericModule

from .enums import Mode


class FmModule(GenericModule):

    class controller_types(object):
        c_volume = Controller(0x01, Range(0, 256))
        m_volume = Controller(0x02, Range(0, 256))
        panning = Controller(0x03, Range(-128, 128))
        c_freq_ratio = Controller(0x04, Range(0, 16))
        m_freq_ratio = Controller(0x05, Range(0, 16))
        m_feedback = Controller(0x06, Range(0, 256))
        c_attack = Controller(0x07, Range(0, 512))
        c_decay = Controller(0x08, Range(0, 512))
        c_sustain = Controller(0x09, Range(0, 256))
        c_release = Controller(0x0a, Range(0, 512))
        m_attack = Controller(0x0b, Range(0, 512))
        m_decay = Controller(0x0c, Range(0, 512))
        m_sustain = Controller(0x0d, Range(0, 256))
        m_release = Controller(0x0e, Range(0, 512))
        m_scaling_per_key = Controller(0x0f, Range(0, 4))
        polyphony_ch = Controller(0x10, Range(1, 16))
        mode = Controller(0x11, Mode)
