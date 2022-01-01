from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.fmx import BaseFmx


class Fmx(BaseFmx, Module):

    chnk = 4

    behaviors = {B.receives_notes, B.sends_audio}

    class custom_waveform_chunk(BaseFmx.custom_waveform_chunk):
        element_size = 4
        python_type = float
        type = "f"

    def __init__(self, **kwargs):
        custom_waveform_values = kwargs.pop("custom_waveform_values", None)
        super(Fmx, self).__init__(**kwargs)
        self.custom_waveform = self.custom_waveform_chunk()
        if custom_waveform_values is not None:
            self.custom_waveform.values = custom_waveform_values

    def specialized_iff_chunks(self):
        yield from self.custom_waveform.chunks()
        yield from super(Fmx, self).specialized_iff_chunks()

    def load_chunk(self, chunk):
        if chunk.chnm == 0:
            self.custom_waveform.bytes = chunk.chdt
