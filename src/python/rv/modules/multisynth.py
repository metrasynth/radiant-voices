from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.multisynth import BaseMultiSynth


class MultiSynth(BaseMultiSynth, Module):

    chnk = 4
    options_chnm = 1

    behaviors = {B.receives_notes, B.sends_notes}

    def __init__(self, **kwargs):
        nv_values = kwargs.pop("nv_values", None)
        vv_values = kwargs.pop("vv_values", None)
        super(MultiSynth, self).__init__(**kwargs)
        self.nv_curve = self.note_velocity_curve_chunk()
        self.vv_curve = self.velocity_velocity_curve_chunk()
        self.np_curve = self.note_pitch_curve_chunk()
        if nv_values is not None:
            self.nv_curve.values = nv_values
        if vv_values is not None:
            self.vv_curve.values = vv_values

    def specialized_iff_chunks(self):
        yield from self.nv_curve.chunks()
        yield from super(MultiSynth, self).specialized_iff_chunks()
        yield from self.vv_curve.chunks()
        yield from self.np_curve.chunks()

    def load_chunk(self, chunk):
        if chunk.chnm == self.options_chnm:
            self.load_options(chunk)
        elif chunk.chnm == 0:
            self.nv_curve.bytes = chunk.chdt
        elif chunk.chnm == 2:
            self.vv_curve.bytes = chunk.chdt
        elif chunk.chnm == 3:
            self.np_curve.bytes = chunk.chdt
