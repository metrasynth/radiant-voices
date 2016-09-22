from enum import Enum

from rv.chunks import CurveChunk
from rv.controller import Controller
from rv.modules import Module


class WaveShaper(Module):

    name = mtype = 'WaveShaper'
    mgroup = 'Effect'
    chnk = 0x10

    class Mode(Enum):
        hq = 0
        hq_mono = 1
        lq = 2
        lq_mono = 3

    class Curve(CurveChunk):
        chnm = 0
        length = 256
        type = 'H'
        default = [x * 0x100 for x in range(256)]

    input_volume = Controller((0, 512), 256)
    mix = Controller((0, 256), 256)
    output_volume = Controller((0, 512), 256)
    symmetric = Controller(bool, True)
    mode = Controller(Mode, Mode.hq)
    dc_blocker = Controller(bool, True)

    def __init__(self, **kwargs):
        values = kwargs.pop('values', None)
        super(WaveShaper, self).__init__(**kwargs)
        self.curve = self.Curve()
        if values is not None:
            self.curve.values = values

    def specialized_iff_chunks(self):
        for chunk in self.curve.chunks():
            yield chunk

    def load_chunk(self, chunk):
        if chunk.chnm == 0:
            self.load_curve(chunk)

    def load_curve(self, chunk):
        self.curve.bytes = chunk.chdt
