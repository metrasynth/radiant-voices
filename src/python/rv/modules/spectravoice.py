from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.spectravoice import BaseSpectraVoice


class SpectraVoice(BaseSpectraVoice, Module):

    chnk = 4

    behaviors = {B.receives_notes, B.sends_audio}

    def __init__(self, **kwargs):
        harmonics = kwargs.pop("harmonics", [])
        super(SpectraVoice, self).__init__(**kwargs)
        self.harmonic_freqs = self.harmonic_freqs_chunk()
        self.harmonic_volumes = self.harmonic_volumes_chunk()
        self.harmonic_widths = self.harmonic_widths_chunk()
        self.harmonic_types = self.harmonic_types_chunk()
        # Initialize harmonics from 'harmonics' kwarg.
        self.harmonics = [Harmonic(self, index) for index in range(16)]
        for i, (freq, volume, width, type) in enumerate(harmonics):
            h = self.harmonics[i]
            h.freq_hz, h.volume, h.width, h.type = freq, volume, width, type
        h = self.harmonics[self.harmonic]
        self.h_freq_hz = h.freq_hz
        self.h_volume = h.volume
        self.h_width = h.width
        self.h_type = h.type

    def specialized_iff_chunks(self):
        yield from self.harmonic_freqs.chunks()
        yield from self.harmonic_volumes.chunks()
        yield from self.harmonic_widths.chunks()
        yield from self.harmonic_types.chunks()
        yield from super(SpectraVoice, self).specialized_iff_chunks()

    def load_chunk(self, chunk):
        if chunk.chnm == 0:
            self.harmonic_freqs.bytes = chunk.chdt
            for h, freq in zip(self.harmonics, self.harmonic_freqs.values):
                h.freq_hz = freq
        elif chunk.chnm == 1:
            self.harmonic_volumes.bytes = chunk.chdt
            for h, volume in zip(self.harmonics, self.harmonic_volumes.values):
                h.volume = volume
        elif chunk.chnm == 2:
            self.harmonic_widths.bytes = chunk.chdt
            for h, width in zip(self.harmonics, self.harmonic_widths.values):
                h.width = width
        elif chunk.chnm == 3:
            self.harmonic_types.bytes = chunk.chdt
            for h, type in zip(self.harmonics, self.harmonic_types.values):
                h.type = type


class Harmonic:
    def __init__(self, module, index):
        self.module = module
        self.index = index
        self._freq_hz = 0
        self._volume = 0
        self._width = 0
        self._type = SpectraVoice.HarmonicType.hsin

    @property
    def freq_hz(self):
        return self._freq_hz

    @freq_hz.setter
    def freq_hz(self, value):
        self._freq_hz = value
        self.module.harmonic_freqs.values[self.index] = value

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value):
        self._volume = value
        self.module.harmonic_volumes.values[self.index] = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value
        self.module.harmonic_widths.values[self.index] = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value
        if isinstance(value, str):
            value = SpectraVoice.HarmonicType[value]
        self.module.harmonic_types.values[self.index] = value
