from enum import Enum

from rv.chunks import ArrayChunk
from rv.controller import Controller
from rv.modules import Behavior as B, Module


class SpectraVoice(Module):

    name = mtype = 'SpectraVoice'
    mgroup = 'Synth'
    chnk = 0x10

    behaviors = {B.receives_notes, B.sends_audio}

    class Mode(Enum):
        hq = 0
        hq_mono = 1
        lq = 2
        lq_mono = 3
        hq_spline = 4

    class HarmonicType(Enum):
        hsin = 0
        rect = 1
        org1 = 2
        org2 = 3
        org3 = 4
        org4 = 5
        sin = 6
        random = 7
        triangle1 = 8
        triangle2 = 9
        overtones1 = 10
        overtones2 = 11
        overtones3 = 12
        overtones4 = 13

    class HarmonicValueArray(ArrayChunk):
        length = 16

    class HarmonicFreqArray(HarmonicValueArray):
        chnm = 0
        type = 'H'
        default = [1098] + [0] * 15
        element_size = 2
        min_value = 0
        max_value = 0x8000

    class HarmonicVolumeArray(HarmonicValueArray):
        chnm = 1
        type = 'B'
        default = [255] + [0] * 15
        element_size = 1
        min_value = 0
        max_value = 0xff

    class HarmonicWidthArray(HarmonicValueArray):
        chnm = 2
        type = 'B'
        default = [3] + [0] * 15
        element_size = 1
        min_value = 0
        max_value = 0xff

    class HarmonicTypeArray(HarmonicValueArray):
        chnm = 3
        type = 'B'
        element_size = 1

        @property
        def default(self):
            return [SpectraVoice.HarmonicType.hsin] * 16

        @property
        def encoded_values(self):
            return [x.value for x in self.values]

        @property
        def python_type(self):
            return SpectraVoice.HarmonicType

    volume = Controller((0, 256), 128)
    panning = Controller((-128, 128), 0)
    attack = Controller((0, 512), 10)
    release = Controller((0, 512), 512)
    polyphony_ch = Controller((1, 32), 8)
    mode = Controller(Mode, Mode.hq_spline)
    sustain = Controller(bool, True)
    spectrum_resolution = Controller((0, 5), 1)
    # Note: These are controllers used to program the module while it's loaded.
    # When scripting, use the objects in `self.harmonics` instead.
    harmonic = Controller((0, 15), 0)
    h_freq_hz = Controller((0, 22050), 1098)
    h_volume = Controller((0, 255), 255)
    h_width = Controller((0, 255), 3)
    h_type = Controller(HarmonicType, HarmonicType.hsin)

    def __init__(self, **kwargs):
        harmonics = kwargs.pop('harmonics', [])
        super(SpectraVoice, self).__init__(**kwargs)
        self.harmonic_freqs = self.HarmonicFreqArray()
        self.harmonic_volumes = self.HarmonicVolumeArray()
        self.harmonic_widths = self.HarmonicWidthArray()
        self.harmonic_types = self.HarmonicTypeArray()
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
        for chunk in self.harmonic_freqs.chunks():
            yield chunk
        for chunk in self.harmonic_volumes.chunks():
            yield chunk
        for chunk in self.harmonic_widths.chunks():
            yield chunk
        for chunk in self.harmonic_types.chunks():
            yield chunk
        for chunk in super(SpectraVoice, self).specialized_iff_chunks():
            yield chunk

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


class Harmonic(object):

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
