from rv.structure.controller import Controller
from rv.structure.module import GenericModule


class Mode(IntEnum):

    HQ = 0
    HQ_MONO = 1
    LQ = 2
    LQ_MONO = 3


class FmModule(GenericModule):

    class controller_types:
        c_volume = Controller(0x01, (0, 256))
        m_volume = Controller(0x02, (0, 256))
        panning = Controller(0x03, (-128, 128))
        c_freq_ratio = Controller(0x04, (0, 16))
        m_freq_ratio = Controller(0x05, (0, 16))
        m_feedback = Controller(0x06, (0, 256))
        c_attack = Controller(0x07, (0, 512))
        c_decay = Controller(0x08, (0, 512))
        c_sustain = Controller(0x09, (0, 256))
        c_release = Controller(0x0a, (0, 512))
        m_attack = Controller(0x0b, (0, 512))
        m_decay = Controller(0x0c, (0, 512))
        m_sustain = Controller(0x0d, (0, 256))
        m_release = Controller(0x0e, (0, 512))
        m_scaling_per_key = Controller(0x0f, (0, 4))
        polyphony_ch = Controller(0x10, (1, 16))
        mode = Controller(0x11, Mode)
