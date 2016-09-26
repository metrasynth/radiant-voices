from itertools import chain

from rv.chunks import ArrayChunk
from rv.controller import Controller
from rv.modules import Module


class MultiCtl(Module):

    name = mtype = 'MultiCtl'
    mgroup = 'Misc'
    chnk = 0x10

    class Mapping(object):
        def __init__(self, value):
            self.min, self.max, self.controller = value[:3]

    class MappingArray(ArrayChunk):
        chnm = 0
        length = 16
        type = 'IIIIIIII'
        element_size = 4 * 8
        @property
        def default(self):
            return [
                MultiCtl.Mapping((0, 0x8000, 0))
                for x in range(self.length)
            ]
        @property
        def encoded_values(self):
            return list(chain.from_iterable(
                (x.min, x.max, x.controller, 0, 0, 0, 0, 0)
                for x in self.values
            ))
        @property
        def python_type(self):
            return MultiCtl.Mapping

    class Curve(ArrayChunk):
        chnm = 1
        length = 257
        type = 'H'
        element_size = 2
        default = [x * 0x80 for x in range(257)]

    value = Controller((0, 32768), 0)
    gain = Controller((0, 1024), 256)
    quantization = Controller((0, 32768), 32768)

    def __init__(self, **kwargs):
        curve = kwargs.pop('curve', None)
        mappings = kwargs.pop('mappings', [])
        super(MultiCtl, self).__init__(**kwargs)
        self.curve = self.Curve()
        if curve is not None:
            self.curve.values = curve
        self.mappings = self.MappingArray()
        for i, mapping in enumerate(mappings):
            self.mappings.values[i] = self.Mapping(mapping)

    def specialized_iff_chunks(self):
        for chunk in self.mappings.chunks():
            yield chunk
        for chunk in self.curve.chunks():
            yield chunk

    def load_chunk(self, chunk):
        if chunk.chnm == 0:
            self.mappings.bytes = chunk.chdt
        if chunk.chnm == 1:
            self.curve.bytes = chunk.chdt
