from struct import pack

from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.vorbisplayer import BaseVorbisPlayer


class VorbisPlayer(BaseVorbisPlayer, Module):

    chnk = 1

    behaviors = {B.sends_audio}

    data = None

    def __init__(self, **kwargs):
        data = kwargs.pop("data", None)
        super(VorbisPlayer, self).__init__(**kwargs)
        self.data = data

    def specialized_iff_chunks(self):
        yield b"CHNM", pack("<I", 0)
        yield b"CHDT", self.data or b""
        yield from super(VorbisPlayer, self).specialized_iff_chunks()

    def load_chunk(self, chunk):
        if chunk.chnm == 0:
            self.data = chunk.chdt
