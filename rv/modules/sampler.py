from collections import OrderedDict
from enum import Enum
from io import BytesIO
from itertools import chain
from struct import pack, unpack

from rv.controller import Controller
from rv.modules import Behavior as B, Module
from rv.note import NOTE
from rv.option import Option


class Sampler(Module):
    """
    ..  note::

        Radiant Voices only supports sampler modules in files that were
        saved using newer versions of SunVox.

        Files created using older versions of SunVox, such as some of the files
        in the ``simple_examples`` included with SunVox, must first be
        loaded into the latest version of SunVox and then saved.
    """

    name = mtype = 'Sampler'
    mgroup = 'Synth'
    chnk = 0x0102
    options_chnm = 0x0101

    behaviors = {B.receives_notes, B.sends_audio}

    class SampleInterpolation(Enum):
        off = 0
        linear = 1
        spline = 2

    class EnvelopeInterpolation(Enum):
        off = 0
        linear = 1

    class VibratoType(Enum):
        sin = 0
        saw = 1
        square = 2

    class LoopType(Enum):
        off = 0
        forward = 1
        ping_pong = 2

    class Format(Enum):
        int8 = 1
        int16 = 2
        float32 = 4

    class Channels(Enum):
        mono = 0
        stereo = 8

    class NoteSampleMap(OrderedDict):
        start_note = NOTE.C0
        end_note = NOTE.a9
        default_sample = 0

        def __init__(self):
            super(Sampler.NoteSampleMap, self).__init__(
                (NOTE(note_value), self.default_sample)
                for note_value in range(self.start_note.value,
                                        self.end_note.value + 1)
            )

        @property
        def bytes(self):
            return bytes(self.values())

        @bytes.setter
        def bytes(self, value):
            for k, v in zip(self.keys(), value):
                self[k] = v

    class Envelope(object):
        length = 12
        range = None
        initial_x_values = None
        initial_y_values = None
        initial_active_points = None
        initial_sustain_point = None
        initial_loop_start_point = None
        initial_loop_end_point = None
        initial_enable = None
        initial_sustain = None
        initial_loop = None
        format = '<' + 'H' * length * 2

        def __init__(self):
            self.x_values = self.initial_x_values.copy()
            self.y_values = self.initial_y_values.copy()
            self.active_points = self.initial_active_points
            self.sustain_point = self.initial_sustain_point
            self.loop_start_point = self.initial_loop_start_point
            self.loop_end_point = self.initial_loop_end_point
            self.enable = self.initial_enable
            self.sustain = self.initial_sustain
            self.loop = self.initial_loop

        @property
        def bitmask(self):
            return self.enable | self.sustain * 2 | self.loop * 4

        @bitmask.setter
        def bitmask(self, value):
            self.enable = bool(value & 1)
            self.sustain = bool(value & 2)
            self.loop = bool(value & 4)

        @property
        def point_bytes(self):
            y_points = (y - self.range[0] for y in self.y_values)
            values = list(chain.from_iterable(zip(self.x_values, y_points)))
            return pack(self.format, *values)

        @point_bytes.setter
        def point_bytes(self, value):
            values = unpack(self.format, value)
            for i in range(self.length):
                x, y = values[i * 2], values[i * 2 + 1]
                y += self.range[0]
                self.x_values[i], self.y_values[i] = x, y

    class VolumeEnvelope(Envelope):
        range = (0, 40)
        initial_active_points = 4
        initial_enable = True
        initial_loop = False
        initial_loop_start_point = 0
        initial_loop_end_point = 0
        initial_sustain = True
        initial_sustain_point = 0
        initial_x_values = [0, 8, 128, 256, 0, 0, 0, 0, 0, 0, 0, 0]
        initial_y_values = [64, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    class PanningEnvelope(Envelope):
        range = (-20, 20)
        initial_active_points = 4
        initial_enable = False
        initial_loop = False
        initial_loop_start_point = 0
        initial_loop_end_point = 0
        initial_sustain = False
        initial_sustain_point = 0
        initial_x_values = [0, 64, 128, 180, 0, 0, 0, 0, 0, 0, 0, 0]
        initial_y_values = [12, -4, 28, 12, -20, -20,
                            -20, -20, -20, -20, -20, -20]

    class Sample(object):
        def __init__(self):
            self.data = b''
            self.loop_start = 0
            self.loop_end = 0
            self.volume = 64
            self.finetune = 100
            self.format = Sampler.Format.float32
            self.channels = Sampler.Channels.stereo
            self.rate = 44100
            self.loop_type = Sampler.LoopType.off
            self.panning = 0
            self.relative_note = 16
            self.unknown6 = b'\0' * 23

        @property
        def frame_size(self):
            size = {Sampler.Format.int8: 1, Sampler.Format.int16: 2,
                    Sampler.Format.float32: 4}
            multiplier = {Sampler.Channels.mono: 1, Sampler.Channels.stereo: 2}
            return size[self.format] * multiplier[self.channels]

        @property
        def frames(self):
            return len(self.data) // self.frame_size

    volume = Controller((0, 512), 256)
    panning = Controller((-128, 128), 0)
    sample_interpolation = Controller(
        SampleInterpolation, SampleInterpolation.spline)
    envelope_interpolation = Controller(
        EnvelopeInterpolation, EnvelopeInterpolation.linear)
    polyphony_ch = Controller((1, 32), 8)
    rec_threshold = Controller((0, 10000), 4)

    vibrato_type = Controller(VibratoType, VibratoType.sin, attached=False)
    vibrato_attack = Controller((0, 255), 0, attached=False)
    vibrato_depth = Controller((0, 255), 0, attached=False)
    vibrato_rate = Controller((0, 63), 0, attached=False)
    volume_fadeout = Controller((0, 8192), 0, attached=False)

    record_on_play = Option(False)
    record_in_mono = Option(False)
    record_with_reduced_sample_rate = Option(False)
    record_in_16_bit = Option(False)
    stop_recording_on_project_stop = Option(False)

    def __init__(self, **kwargs):
        super(Sampler, self).__init__(**kwargs)
        self.volume_envelope = self.VolumeEnvelope()
        self.panning_envelope = self.PanningEnvelope()
        self.note_samples = self.NoteSampleMap()
        self.samples = [None] * 128
        self.unknown1 = b'\0' * 28
        self.unknown2 = b'\0' * 4
        self.unknown3 = b'\x40\x00\x80\x00\x00\x00\x00\x00'
        self.unknown4 = b'\x04\x00\x00\x00'
        self.unknown5 = b'\0' * 9

    def specialized_iff_chunks(self):
        for chunk in self.envelope_chunks():
            yield chunk
        for chunk in super(Sampler, self).specialized_iff_chunks():
            yield chunk
        for i, sample in enumerate(self.samples):
            if sample is not None:
                for chunk in self.sample_chunks(i, sample):
                    yield chunk

    def envelope_chunks(self):
        f = BytesIO()
        w = f.write

        def b(v):
            return pack('<B', v)

        w(self.unknown1)
        compacted_samples = self.samples.copy()
        while compacted_samples and compacted_samples[-1] is None:
            compacted_samples.pop()
        w(pack('<I', len(compacted_samples)))
        w(self.unknown2)
        w(self.note_samples.bytes[:96])
        vol = self.volume_envelope
        pan = self.panning_envelope
        w(vol.point_bytes)
        w(pan.point_bytes)
        w(b(vol.active_points))
        w(b(pan.active_points))
        w(b(vol.sustain_point))
        w(b(vol.loop_start_point))
        w(b(vol.loop_end_point))
        w(b(pan.sustain_point))
        w(b(pan.loop_start_point))
        w(b(pan.loop_end_point))
        w(b(vol.bitmask))
        w(b(pan.bitmask))
        w(b(self.vibrato_type.value))
        w(b(self.vibrato_attack))
        w(b(self.vibrato_depth))
        w(b(self.vibrato_rate))
        w(pack('<H', self.volume_fadeout))
        w(self.unknown3)
        w(b'PMAS')
        w(self.unknown4)
        w(self.note_samples.bytes)
        w(self.unknown5)
        yield (b'CHNM', pack('<I', 0))
        yield (b'CHDT', f.getvalue())
        f.close()
        yield (b'CHFF', pack('<I', 0))
        yield (b'CHFR', pack('<I', 0))

    def sample_chunks(self, i, sample):
        f = BytesIO()
        w = f.write
        w(pack('<I', sample.frames))
        w(pack('<I', sample.loop_start))
        w(pack('<I', sample.loop_end))
        w(pack('<B', sample.volume))
        w(pack('<b', sample.finetune))
        format_flag = {self.Format.int8: 0x00, self.Format.int16: 0x10,
                       self.Format.float32: 0x20}[sample.format]
        channels_flag = {self.Channels.mono: 0x00,
                         self.Channels.stereo: 0x40}[sample.channels]
        loop_format_flags = \
            sample.loop_type.value | format_flag | channels_flag
        w(pack('<B', loop_format_flags))
        w(pack('<B', sample.panning + 0x80))
        w(pack('<b', sample.relative_note))
        w(sample.unknown6)
        yield (b'CHNM', pack('<I', i * 2 + 1))
        yield (b'CHDT', f.getvalue())
        f.close()
        yield (b'CHFF', pack('<I', 0))
        yield (b'CHFR', pack('<I', 0))
        yield (b'CHNM', pack('<I', i * 2 + 2))
        yield (b'CHDT', sample.data)
        yield (b'CHFF', pack(
            '<I', sample.format.value | sample.channels.value))
        yield (b'CHFR', pack('<I', sample.rate))

    def load_chunk(self, chunk):
        if chunk.chnm == self.options_chnm:
            self.load_options(chunk)
        elif chunk.chnm == 0:
            self.load_envelopes(chunk)
        elif chunk.chnm % 2 == 1:
            self.load_sample_meta(chunk)
        elif chunk.chnm % 2 == 0:
            self.load_sample_data(chunk)

    def load_envelopes(self, chunk):
        data = chunk.chdt
        vol = self.volume_envelope
        pan = self.panning_envelope
        vol.point_bytes = data[0x84:0xb4]
        pan.point_bytes = data[0xb4:0xe4]
        vol.active_points = data[0xe4]
        pan.active_points = data[0xe5]
        vol.sustain_point = data[0xe6]
        vol.loop_start_point = data[0xe7]
        vol.loop_end_point = data[0xe8]
        pan.sustain_point = data[0xe9]
        pan.loop_start_point = data[0xea]
        pan.loop_end_point = data[0xeb]
        vol.bitmask = data[0xec]
        pan.bitmask = data[0xed]
        self.vibrato_type = self.VibratoType(data[0xee])
        self.vibrato_attack = data[0xef]
        self.vibrato_depth = data[0xf0]
        self.vibrato_rate = data[0xf1]
        self.volume_fadeout, = unpack('<H', data[0xf2:0xf4])
        self.note_samples.bytes = data[0x104:0x17b]
        self.unknown1 = data[0x00:0x1c]
        self.unknown2 = data[0x20:0x24]
        self.unknown3 = data[0xf4:0xfc]
        self.unknown4 = data[0x100:0x104]
        self.unknown5 = data[0x17b:0x184]

    def load_sample_meta(self, chunk):
        index = (chunk.chnm - 1) // 2
        sample = self.samples[index] = self.Sample()
        data = chunk.chdt
        sample.loop_start, = unpack('<I', data[0x04:0x08])
        sample.loop_end, = unpack('<I', data[0x08:0x0c])
        sample.volume = data[0x0c]
        sample.finetune, = unpack('<b', data[0x0d:0x0e])
        loop_format_flags = data[0x0e]
        loop = loop_format_flags & (0 | 1 | 2)
        sample.loop_type = self.LoopType(loop)
        format = loop_format_flags & (0x00 | 0x10 | 0x20)
        sample.format = {0x00: self.Format.int8, 0x10: self.Format.int16,
                         0x20: self.Format.float32}[format]
        if loop_format_flags & 0x40:
            sample.channels = self.Channels.stereo
        else:
            sample.channels = self.Channels.mono
        sample.panning = data[0x0f] - 0x80
        sample.relative_note, = unpack('<b', data[0x10:0x11])
        sample.unknown6 = data[0x11:0x28]

    def load_sample_data(self, chunk):
        index = (chunk.chnm - 2) // 2
        sample = self.samples[index]
        sample.data = chunk.chdt
        sample.format = self.Format(chunk.chff & 0x07)
        sample.channels = self.Channels(chunk.chff & 0x08)
        sample.rate = chunk.chfr


"""
                0  1  2  3  4  5  6  7   8  9  a  b  c  d  e  f
CHNM: 00000000
CHDT: 00000000: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
                ------------------------------------------------ unknown1
      00000010: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
                ------------------------------------ unknown1
                                                     ----------- max sample index + 1
                                                                 (0 for no samples)
      00000020: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
                ----------- unknown2
                            -- sample number for note C-0 (note 0)
      00000030: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
      00000040: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
      00000050: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
      00000060: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
      00000070: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
      00000080: 00 00 00 00 00 00 40 00  08 00 00 00 80 00 00 00  ......@.........
                         -- sample number for note B-8 (note 95)
                            ----- vol envelope: point 1 x position (always 0)
                                  ----- vol envelope: point 1 y position (00-40)
                                         ----- vol point 2 x
                                               ----- vol point 2 y
                                                     ----- vol point 3 x
                                                           ----- vol point 3 y
      00000090: 00 01 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
                ----- point 4 x
                      ----- vol point 4 y
                            ----- vol point 5 x
                                  ----- vol point 5 y
                                         ----- vol point 6 x
                                               ----- vol point 6 y
                                                     ----- vol point 7 x
                                                           ----- vol point 7 y
      000000A0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
                ----- vol point 8 x
                      ----- vol point 8 y
                            ----- vol point 9 x
                                  ----- vol point 9 y
                                         ----- vol point 10 x
                                               ----- vol point 10 y
                                                     ----- vol point 11 x
                                                           ----- vol point 11 y
                0  1  2  3  4  5  6  7   8  9  a  b  c  d  e  f
      000000B0: 00 00 00 00 00 00 20 00  40 00 10 00 80 00 30 00  ...... .@.....0.
                ----- vol point 12 x
                      ----- vol point 12 y
                            ----- panning envelope: point 1 x position (always 0)
                                  ----- panning envelope: point 1 y position (00-40, 20=center)
                                         ----- pan point 2 x
                                               ----- pan point 2 y
                                                     ----- pan point 3 x
                                                           ----- pan point 3 y
      000000C0: B4 00 20 00 00 00 00 00  00 00 00 00 00 00 00 00  .. .............
                ----- point 4 x
                      ----- pan point 4 y
                            ----- pan point 5 x
                                  ----- pan point 5 y
                                         ----- pan point 6 x
                                               ----- pan point 6 y
                                                     ----- pan point 7 x
                                                           ----- pan point 7 y
      000000D0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
                ----- pan point 8 x
                      ----- pan point 8 y
                            ----- pan point 9 x
                                  ----- pan point 9 y
                                         ----- pan point 10 x
                                               ----- pan point 10 y
                                                     ----- pan point 11 x
                                                           ----- pan point 11 y
                0  1  2  3  4  5  6  7   8  9  a  b  c  d  e  f
      000000E0: 00 00 00 00 04 04 00 00  00 00 00 00 03 00 00 00  ................
                ----- pan point 12 x
                      ----- pan point 12 y
                            -- number of active vol envelope points
                               -- number of active pan envelope points
                                  -- vol sustain point
                                     -- vol loop start point
                                         -- vol loop end point
                                            -- pan sustain point
                                               -- pan loop start point
                                                  -- pan loop end point
                                                     -- volume envelope bitmask: 1 = enable, 2 = sustain, 4 = loop
                                                        -- panning envelope bitmask: 1 = enable, 2 = sustain, 4 = loop
                                                           -- vibrato type: 0=sin, 1=saw, 2=square
                                                              -- vibrato attack (0-255)
      000000F0: 00 00 00 00 40 00 80 00  00 00 00 00 50 4D 41 53  ....@.......PMAS
                -- vibrato depth (0-255)
                   -- vibrato rate (0-63)
                      ----- volume fadeout (0-8192)
                            ------------------------ unknown3
                                                     ----------- magic (little-endian SAMP)
      00000100: 04 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
                ----------- unknown4
                            -- sample number for note C-0 (note 0)
      00000110: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
      00000120: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
      00000130: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
      00000140: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
      00000150: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
      00000160: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
      00000170: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
                0  1  2  3  4  5  6  7   8  9  a  b  c  d  e  f
                                               -- sample number for note b-9 (note 118)
                                                  -------------- unknown5
      00000180: 00 00 00 00                                       ....
                ----------- unknown5

CHNM: (sample number * 2 + 1)
                0  1  2  3  4  5  6  7   8  9  a  b  c  d  e  f
CHDT: 00000000: C7 08 00 00 00 00 00 00  00 00 00 00 40 64 00 80  ............@d..
                ----------- length (frames)
                            ----------- loop start frame
                                         ----------- loop end frame
                                                     -- volume (0-64)
                                                        -- finetune (-128-127, signed, center=0x00)
                                                           -- 0x_0 = no loop
                                                           -- 0x_1 = loop
                                                           -- 0x_2 = ping-pong loop
                                                           -- 0x0_ = 8-bit mono
                                                           -- 0x1_ = 16-bit mono
                                                           -- 0x2_ = 32-bit mono
                                                           -- add 0x40 for stereo
                                                              -- panning (-128-127, 0x00-0xFF, unsigned w/ offset, center = 0x80)
      00000010: 10 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
                -- relative note (-128-127, signed, center=0x00)
                   --------------------------------------------- unknown6
      00000020: 00 00 00 00 00 00 00 00                           ........
                ----------------------- unknown6
CHFF: 0
CHFR: 0

CHNM: (sample number * 2 + 2)
CHDT: <sample data, signed>
CHFF: format:
        1 - 8-bit mono
        2 - 16-bit mono
        4 - 32-bit mono
        9 - 8-bit stereo
        A - 16-bit stereo
        C - 32-bit stereo
CHFR: sample rate
"""  # NOQA
