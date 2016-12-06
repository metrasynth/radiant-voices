from struct import pack

from rv.controller import Controller
from rv.modules import Behavior as B, Module


class VorbisPlayer(Module):

    name = mtype = 'Vorbis player'
    mgroup = 'Synth'
    chnk = 0x10

    behaviors = {B.sends_audio}

    data = None

    volume = Controller((0, 512), 256)
    original_speed = Controller(bool, True)
    finetune = Controller((-128, 128), 0)
    transpose = Controller((-128, 128), 0)
    interpolation = Controller(bool, True)
    polyphony_ch = Controller((1, 4), 1)
    repeat = Controller(bool, False)

    def __init__(self, **kwargs):
        data = kwargs.pop('data', None)
        super(VorbisPlayer, self).__init__(**kwargs)
        self.data = data

    def specialized_iff_chunks(self):
        yield (b'CHNM', pack('<I', 0))
        yield (b'CHDT', self.data or b'')
        yield (b'CHFF', pack('<I', 0))
        yield (b'CHFR', pack('<I', 0))
        for chunk in super(VorbisPlayer, self).specialized_iff_chunks():
            yield chunk

    def load_chunk(self, chunk):
        if chunk.chnm == 0:
            self.data = chunk.chdt
