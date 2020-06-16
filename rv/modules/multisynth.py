from rv.chunks import ArrayChunk
from rv.controller import Controller, CompactRange
from rv.modules import Behavior as B, Module
from rv.option import Option


class MultiSynth(Module):

    name = mtype = "MultiSynth"
    mgroup = "Misc"
    chnk = 3
    options_chnm = 1
    flags = 0x021049

    behaviors = {B.receives_notes, B.sends_notes}

    class NoteVelocityCurve(ArrayChunk):
        chnm = 0
        length = 128
        type = "B"
        element_size = 1
        default = 0xFF
        min_value = 0
        max_value = 0xFF

    class VelocityVelocityCurve(ArrayChunk):
        chnm = 2
        length = 257
        type = "B"
        element_size = 1
        min_value = 0
        max_value = 0xFF

        def default(self, x):
            return min(x, 255)

    transpose = Controller(CompactRange(-128, 128), 0)
    random_pitch = Controller((0, 4096), 0)
    velocity = Controller((0, 256), 256)
    finetune = Controller((-256, 256), 0)
    random_phase = Controller((0, 32768), 0)
    random_velocity = Controller((0, 32768), 0)
    phase = Controller((0, 32768), 0)
    curve2_influence = Controller((0, 256), 256)

    use_static_note_C5 = Option(False)
    ignore_notes_with_zero_velocity = Option(False)
    vv_curve_active = Option(False)
    trigger = Option(False)

    def __init__(self, **kwargs):
        nv_values = kwargs.pop("nv_values", None)
        vv_values = kwargs.pop("vv_values", None)
        super(MultiSynth, self).__init__(**kwargs)
        self.nv_curve = self.NoteVelocityCurve()
        self.vv_curve = self.VelocityVelocityCurve()
        if nv_values is not None:
            self.nv_curve.values = nv_values
        if vv_values is not None:
            self.vv_curve.values = vv_values

    def specialized_iff_chunks(self):
        yield from self.nv_curve.chunks()
        yield from super(MultiSynth, self).specialized_iff_chunks()
        yield from self.vv_curve.chunks()

    def load_chunk(self, chunk):
        if chunk.chnm == self.options_chnm:
            self.load_options(chunk)
        elif chunk.chnm == 0:
            self.nv_curve.bytes = chunk.chdt
        elif chunk.chnm == 2:
            self.vv_curve.bytes = chunk.chdt
