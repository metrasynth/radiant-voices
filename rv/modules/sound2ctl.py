from enum import Enum

from rv.controller import Controller
from rv.modules import Behavior as B, Module
from rv.option import Option


class Sound2Ctl(Module):

    name = mtype = 'Sound2Ctl'
    mgroup = 'Misc'
    chnk = 0x10
    options_chnm = 0x00

    class Channels(Enum):
        mono = 0
        stereo = 1

    class Mode(Enum):
        lq = 0
        hq = 1

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

    record_values = Option(False)

    def load_chunk(self, chunk):
        if chunk.chnm == self.options_chnm:
            self.load_options(chunk)
