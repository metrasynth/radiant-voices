from rv.chunks import CurveChunk
from rv.controller import Controller
from rv.modules import Module
from rv.option import Option


class MultiSynth(Module):

    name = mtype = 'MultiSynth'
    mgroup = 'Misc'
    chnk = 0x10
    options_chnm = 1

    class NoteVelocityCurve(CurveChunk):
        chnm = 0
        length = 128
        type = 'B'
        default = [0xff] * length

    class VelocityVelocityCurve(CurveChunk):
        chnm = 2
        length = 257
        type = 'B'
        default = list(range(256)) + [0xff]

    transpose = Controller((-128, 128), 0)
    random_pitch = Controller((0, 4096), 0)
    velocity = Controller((0, 256), 256)
    finetune = Controller((-256, 256), 0)
    random_phase = Controller((0, 32768), 0)
    random_velocity = Controller((0, 32768), 0)
    phase = Controller((0, 32768), 0)

    use_static_note_C5 = Option(False)
    ignore_notes_with_zero_velocity = Option(False)
    vv_curve_active = Option(False)

    def __init__(self, **kwargs):
        nv_values = kwargs.pop('nv_values', None)
        vv_values = kwargs.pop('vv_values', None)
        super(MultiSynth, self).__init__(**kwargs)
        self.nv_curve = self.NoteVelocityCurve()
        self.vv_curve = self.VelocityVelocityCurve()
        if nv_values is not None:
            self.nv_curve.values = nv_values
        if vv_values is not None:
            self.vv_curve.values = vv_values

    def specialized_iff_chunks(self):
        for chunk in self.nv_curve.chunks():
            yield chunk
        for chunk in self.vv_curve.chunks():
            yield chunk

    def load_chunk(self, chunk):
        if chunk.chnm == self.options_chnm:
            self.load_options(chunk)
        elif chunk.chnm == 0:
            self.load_nv_curve(chunk)
        elif chunk.chnm == 2:
            self.load_vv_curve(chunk)

    def load_nv_curve(self, chunk):
        self.nv_curve.bytes = chunk.chdt

    def load_vv_curve(self, chunk):
        self.vv_curve.bytes = chunk.chdt
