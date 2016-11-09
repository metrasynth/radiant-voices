from itertools import chain

from rv.chunks import ArrayChunk
from rv.controller import Controller, Range
from rv.modules import Module


def convert_value(gain, qsteps, smin, smax, dmin, dmax, value):
    # Is the source range inverted?
    if smin > smax:
        inverse = True
        smin, smax = smax, smin
    else:
        inverse = False
    # At a minimum, we need 2 quantization steps (on/off).
    # We also need no more steps then there are values in the source range.
    srange = smax - smin
    qsteps = max(qsteps, 2)
    qsteps = min(qsteps, srange)
    # Apply gain.
    value = value * gain / 256
    # Translate value from full 0-32768 range to source range.
    ratio = value / 32768
    value = srange * ratio + smin
    # Quantize.
    delta = srange // (qsteps - 1)
    value = (value // delta) * delta
    # Limit destination range.
    drange = dmax - dmin
    dmin2 = dmin + drange * (smin / 32768)
    dmax2 = dmin + drange * (smax / 32768)
    drange2 = dmax2 - dmin2
    # Transform from source range to destination range.
    factor = drange2 / srange
    result = (value - smin) * factor + dmin2
    # Invert if necessary.
    if inverse:
        result = dmax2 - result + dmin2
    result = min(result, dmax2)
    result = max(result, dmin2)
    return round(result)


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
            return [MultiCtl.Mapping((0, 0x8000, 0))
                    for x in range(self.length)]

        @property
        def encoded_values(self):
            return list(chain.from_iterable(
                (x.min, x.max, x.controller, 0, 0, 0, 0, 0)
                for x in self.values))

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
    out_offset = Controller((-16384, 16384), 0)

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

    def on_value_changed(self, value, down, up):
        if self.parent is not None and down:
            downstream_mods = []
            for to_mod in range(256):
                from_mods = self.parent.module_connections[to_mod]
                if self.index in from_mods:
                    downstream_mods.append(to_mod)
            for i, to_mod in enumerate(downstream_mods):
                mapping = self.mappings.values[i]
                mod = self.parent.modules[to_mod]
                ctl = list(mod.controllers.values())[mapping.controller - 1]
                if isinstance(ctl.value_type, Range):
                    value = convert_value(
                        self.gain, self.quantization, mapping.min, mapping.max,
                        ctl.value_type.min, ctl.value_type.max, self.value)
                    setattr(mod, ctl.name, value)

    def specialized_iff_chunks(self):
        for chunk in self.mappings.chunks():
            yield chunk
        for chunk in self.curve.chunks():
            yield chunk
        for chunk in super(MultiCtl, self).specialized_iff_chunks():
            yield chunk

    def load_chunk(self, chunk):
        if chunk.chnm == 0:
            self.mappings.bytes = chunk.chdt
        if chunk.chnm == 1:
            self.curve.bytes = chunk.chdt
