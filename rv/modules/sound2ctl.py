from rv.controller import Controller
from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.sound2ctl import BaseSound2Ctl


class Sound2Ctl(BaseSound2Ctl, Module):

    chnk = 1
    options_chnm = 0
    flags = 0x600051

    Channels = BaseSound2Ctl.Channels
    Mode = BaseSound2Ctl.Mode

    behaviors = {B.receives_audio, B.sends_controls}

    sample_rate_hz = Controller((1, 32768), 50)
    channels = Controller(Channels, Channels.mono)
    absolute = Controller(bool, True)
    gain = Controller((0, 1024), 256)
    smooth = Controller((0, 256), 128)
    mode = Controller(Mode, Mode.hq)
    out_min = Controller((0, 32768), 0)
    out_max = Controller((0, 32768), 32768)
    out_controller = Controller((0, 32), 0)

    def load_chunk(self, chunk):
        if chunk.chnm == self.options_chnm:
            self.load_options(chunk)
