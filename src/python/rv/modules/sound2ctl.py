from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.sound2ctl import BaseSound2Ctl


class Sound2Ctl(BaseSound2Ctl, Module):

    chnk = 1
    options_chnm = 0

    behaviors = {B.receives_audio, B.sends_controls}

    def load_chunk(self, chunk):
        if chunk.chnm == self.options_chnm:
            self.load_options(chunk)
