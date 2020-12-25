import logging
from io import BytesIO
from itertools import chain
from struct import pack, unpack
from typing import List, Optional

from logutils import BraceMessage as _F
from rv.controller import Controller
from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.sampler import BaseSampler
from rv.note import NOTE
from rv.readers.reader import read_sunvox_file
from rv.synth import Synth

log = logging.getLogger(__name__)


class Sampler(BaseSampler, Module):
    """
    ..  note::

        Radiant Voices only supports sampler modules in files that were
        saved using newer versions of SunVox.

        Files created using older versions of SunVox, such as some of the files
        in the ``simple_examples`` included with SunVox, must first be
        loaded into the latest version of SunVox and then saved.
    """

    chnk = 0x109
    options_chnm = 0x0101

    behaviors = {B.receives_notes, B.sends_audio}

    effect: Optional[Synth]

    class NoteSampleMap(dict):
        start_note = NOTE.C0
        end_note = NOTE.a9
        default_sample = 0

        def __init__(self):
            super(Sampler.NoteSampleMap, self).__init__(
                (NOTE(note_value), self.default_sample)
                for note_value in range(self.start_note.value, self.end_note.value + 1)
            )

        @property
        def bytes(self):
            return bytes(self.values())

        @bytes.setter
        def bytes(self, value):
            for k, v in zip(self.keys(), value):
                self[k] = v

    class Envelope:
        chnm = None
        range = None
        initial_points = None
        initial_sustain_point = None
        initial_loop_start_point = None
        initial_loop_end_point = None
        initial_enable = None
        initial_sustain = None
        initial_loop = None
        initial_ctl_index = 0
        initial_gain_pct = 100
        initial_velocity = 0
        initial_controller = 0
        _legacy_point_bytes = None
        _legacy_active_points = None
        _legacy_sustain_point = None
        _legacy_loop_start_point = None
        _legacy_loop_end_point = None
        _legacy_bitmask = None

        def __init__(self):
            self.points = self.initial_points[:]
            self.sustain_point = self.initial_sustain_point
            self.loop_start_point = self.initial_loop_start_point
            self.loop_end_point = self.initial_loop_end_point
            self.enable = self.initial_enable
            self.sustain = self.initial_sustain
            self.loop = self.initial_loop
            self.ctl_index = self.initial_ctl_index
            self.gain_pct = self.initial_gain_pct
            self.velocity = self.initial_velocity
            self.loaded = False

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
            y_points = (y - self.range[0] // 0x200 for y in self._y_values)
            values = list(chain.from_iterable(zip(self._x_values, y_points)))
            return pack("<" + "H" * len(values), *values)

        @property
        def _x_values(self):
            values = [x for x, y in self.points]
            while len(values) < 12:
                values.append(0)
            return values[:12]

        @property
        def _y_values(self):
            values = [y // 0x200 for x, y in self.points]
            while len(values) < 12:
                values.append(0)
            return values[:12]

        def chunks(self):
            yield b"CHNM", pack("<I", self.chnm)
            data = pack(
                "<HBBB",
                self.bitmask,
                self.ctl_index,
                self.gain_pct,
                self.velocity,
            )
            data += b"\0\0\0"
            data += pack(
                "<HHHH",
                len(self.points),
                self.sustain_point,
                self.loop_start_point,
                self.loop_end_point,
            )
            data += b"\0\0\0\0"
            for x, y in self.points:
                y -= self.range[0]
                data += pack("<HH", x, y)
            yield b"CHDT", data

        def load_chdt(self, chdt):
            (
                self.bitmask,
                self.ctl_index,
                self.gain_pct,
                self.velocity,
                _,
                _,
                _,
                point_count,
                self.sustain_point,
                self.loop_start_point,
                self.loop_end_point,
            ) = unpack("<HBBBBBBHHHH", chdt[0:0x10])
            points = self.points = []
            for i in range(point_count):
                offset = 0x14 + i * 4
                data = chdt[offset : offset + 4]
                x, y = unpack("<HH", data)
                min_y = self.range[0]
                points.append((x, y + min_y))
            self.loaded = True

    class VolumeEnvelope(Envelope):
        chnm = 0x102
        range = (0, 0x8000)
        initial_enable = True
        initial_loop = False
        initial_loop_start_point = 0
        initial_loop_end_point = 0
        initial_sustain = True
        initial_sustain_point = 0
        initial_points = [(0, 0x8000), (8, 0), (0x80, 0), (0x100, 0)]

    class PanningEnvelope(Envelope):
        chnm = 0x103
        range = (-0x4000, 0x4000)
        initial_enable = False
        initial_loop = False
        initial_loop_start_point = 0
        initial_loop_end_point = 0
        initial_sustain = False
        initial_sustain_point = 0
        initial_points = [(0, 0), (0x40, -0x2000), (0x80, 0x2000), (0xB4, 0)]

    class PitchEnvelope(Envelope):
        chnm = 0x104
        range = (-0x4000, 0x4000)
        initial_enable = False
        initial_loop = False
        initial_loop_start_point = 0
        initial_loop_end_point = 0
        initial_sustain = False
        initial_sustain_point = 0
        initial_points = [(0, 0), (0x40, 0)]

    class EffectControlEnvelope(Envelope):
        range = (0, 0x8000)
        initial_enable = False
        initial_loop = False
        initial_loop_start_point = 0
        initial_loop_end_point = 0
        initial_sustain = False
        initial_sustain_point = 0
        initial_points = [(0, 0x8000), (0x40, 0x8000)]

        def __init__(self, chnm):
            super().__init__()
            self.chnm = chnm

    class Sample:
        def __init__(self):
            self.data = b""
            self.loop_start = 0
            self.loop_len = 0
            self.volume = 64
            self.finetune = 100
            self.format = Sampler.Format.float32
            self.channels = Sampler.Channels.stereo
            self.rate = 44100
            self.loop_type = Sampler.LoopType.off
            self.loop_sustain = False
            self.panning = 0
            self.relative_note = 16
            self.unknown6 = b"\0" * 23

        @property
        def frame_size(self):
            size = {
                Sampler.Format.int8: 1,
                Sampler.Format.int16: 2,
                Sampler.Format.float32: 4,
            }
            multiplier = {Sampler.Channels.mono: 1, Sampler.Channels.stereo: 2}
            return size[self.format] * multiplier[self.channels]

        @property
        def frames(self):
            return len(self.data) // self.frame_size

    vibrato_type = Controller(
        BaseSampler.VibratoType, BaseSampler.VibratoType.sin, attached=False
    )
    vibrato_attack = Controller((0, 255), 0, attached=False)
    vibrato_depth = Controller((0, 255), 0, attached=False)
    vibrato_rate = Controller((0, 63), 0, attached=False)
    volume_fadeout = Controller((0, 8192), 0, attached=False)

    samples: List[Optional[Sample]]

    def __init__(self, **kwargs):
        super(Sampler, self).__init__(**kwargs)
        self.volume_envelope = self.VolumeEnvelope()
        self.panning_envelope = self.PanningEnvelope()
        self.pitch_envelope = self.PitchEnvelope()
        self.effect_control_envelopes = [
            self.EffectControlEnvelope(0x105),
            self.EffectControlEnvelope(0x106),
            self.EffectControlEnvelope(0x107),
            self.EffectControlEnvelope(0x108),
        ]
        self.note_samples = self.NoteSampleMap()
        self.samples = [None] * 128
        self.unknown1 = b"\0" * 28
        self.unknown2 = b"\0" * 4
        self.unknown3 = b"\x40\x00\x80\x00\x00\x00\x00\x00"
        self.unknown4 = b"\x04\x00\x00\x00"
        self.unknown5 = b"\0" * 9
        self.effect = None

    def specialized_iff_chunks(self):
        iters = [
            self.global_config_chunks(),
            self.envelope_config_chunks(),
            self.volume_envelope.chunks(),
            self.panning_envelope.chunks(),
            self.pitch_envelope.chunks(),
            self.effect_control_envelopes[0].chunks(),
            self.effect_control_envelopes[1].chunks(),
            self.effect_control_envelopes[2].chunks(),
            self.effect_control_envelopes[3].chunks(),
        ]
        for iter in iters:
            yield from iter
        if self.effect:
            f = BytesIO()
            self.effect.write_to(f)
            yield b"CHNM", b"\x0a\1\0\0"
            yield b"CHDT", f.getvalue()
        yield from super(Sampler, self).specialized_iff_chunks()
        for i, sample in enumerate(self.samples):
            if sample is not None:
                yield from self.sample_chunks(i, sample)

    def global_config_chunks(self):
        def b(v):
            return pack("<B", v)

        f = BytesIO()
        w = f.write
        w(self.unknown1)
        compacted_samples = self.samples.copy()
        while compacted_samples and compacted_samples[-1] is None:
            compacted_samples.pop()
        w(pack("<I", len(compacted_samples)))
        w(self.unknown2)
        w(self.note_samples.bytes[:96])
        vol = self.volume_envelope
        pan = self.panning_envelope
        w(vol.point_bytes)
        w(pan.point_bytes)
        w(b(len(vol.points)))
        w(b(len(pan.points)))
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
        w(pack("<H", self.volume_fadeout))
        w(self.unknown3)
        w(b"PMAS")
        w(self.unknown4)
        w(self.note_samples.bytes)
        w(self.unknown5)
        yield b"CHNM", pack("<I", 0)
        yield b"CHDT", f.getvalue()
        f.close()

    def envelope_config_chunks(self):
        yield b"CHNM", pack("<I", 0x101)
        yield b"CHDT", b"\x00\x00\x00\x00\x00\x00"

    def sample_chunks(self, i, sample):
        f = BytesIO()
        w = f.write
        w(pack("<I", sample.frames))
        w(pack("<I", sample.loop_start))
        w(pack("<I", sample.loop_len))
        w(pack("<B", sample.volume))
        w(pack("<b", sample.finetune))
        sustain_flag = 4 if sample.loop_sustain else 0
        format_flag = {
            self.Format.int8: 0x00,
            self.Format.int16: 0x10,
            self.Format.float32: 0x20,
        }[sample.format]
        channels_flag = {self.Channels.mono: 0x00, self.Channels.stereo: 0x40}[
            sample.channels
        ]
        loop_format_flags = (
            sample.loop_type.value | format_flag | channels_flag | sustain_flag
        )
        w(pack("<B", loop_format_flags))
        w(pack("<B", sample.panning + 0x80))
        w(pack("<b", sample.relative_note))
        w(sample.unknown6)
        yield b"CHNM", pack("<I", i * 2 + 1)
        yield b"CHDT", f.getvalue()
        f.close()
        yield b"CHNM", pack("<I", i * 2 + 2)
        yield b"CHDT", sample.data
        yield b"CHFF", pack("<I", sample.format.value | sample.channels.value)
        if sample.rate != 44100:
            yield b"CHFR", pack("<I", sample.rate)

    def load_chunk(self, chunk):
        chnm = chunk.chnm
        chdt = chunk.chdt
        if chnm == self.options_chnm:
            self.load_options(chunk)
        elif chnm == 0:
            self.load_envelopes(chunk)
        elif chnm < 0x101 and chnm % 2 == 1:
            self.load_sample_meta(chunk)
        elif chnm < 0x101 and chnm % 2 == 0:
            self.load_sample_data(chunk)
        elif chnm == 0x101:
            self._unknown_0x101 = chdt
        elif chnm == 0x102:
            self.volume_envelope.load_chdt(chdt)
        elif chnm == 0x103:
            self.panning_envelope.load_chdt(chdt)
        elif chnm == 0x104:
            self.pitch_envelope.load_chdt(chdt)
        elif 0x105 <= chnm <= 0x108:
            self.effect_control_envelopes[chnm - 0x105].load_chdt(chdt)
        elif chnm == 0x10A:
            self.effect = read_sunvox_file(BytesIO(chdt))

    def load_envelopes(self, chunk):
        data = chunk.chdt
        vol = self.volume_envelope
        pan = self.panning_envelope
        vol._legacy_point_bytes = data[0x84:0xB4]
        pan._legacy_point_bytes = data[0xB4:0xE4]
        vol._legacy_active_points = data[0xE4]
        pan._legacy_active_points = data[0xE5]
        vol._legacy_sustain_point = data[0xE6]
        vol._legacy_loop_start_point = data[0xE7]
        vol._legacy_loop_end_point = data[0xE8]
        pan._legacy_sustain_point = data[0xE9]
        pan._legacy_loop_start_point = data[0xEA]
        pan._legacy_loop_end_point = data[0xEB]
        vol._legacy_bitmask = data[0xEC]
        pan._legacy_bitmask = data[0xED]
        self.vibrato_type = self.VibratoType(data[0xEE])
        self.vibrato_attack = data[0xEF]
        self.vibrato_depth = data[0xF0]
        self.vibrato_rate = data[0xF1]
        (self.volume_fadeout,) = unpack("<H", data[0xF2:0xF4])
        self.note_samples.bytes = data[0x104:0x17B]
        self.unknown1 = data[0x00:0x1C]
        self.unknown2 = data[0x20:0x24]
        self.unknown3 = data[0xF4:0xFC]
        self.unknown4 = data[0x100:0x104]
        self.unknown5 = data[0x17B:0x184]

    def load_sample_meta(self, chunk):
        index = (chunk.chnm - 1) // 2
        sample = self.samples[index] = self.Sample()
        data = chunk.chdt
        (sample.loop_start,) = unpack("<I", data[0x04:0x08])
        (sample.loop_len,) = unpack("<I", data[0x08:0x0C])
        sample.volume = data[0x0C]
        (sample.finetune,) = unpack("<b", data[0x0D:0x0E])
        loop_format_flags = data[0x0E]
        loop = loop_format_flags & (0 | 1 | 2)
        sample.loop_type = self.LoopType(loop)
        format = loop_format_flags & (0x00 | 0x10 | 0x20)
        sample.format = {
            0x00: self.Format.int8,
            0x10: self.Format.int16,
            0x20: self.Format.float32,
        }[format]
        if loop_format_flags & 0x40:
            sample.channels = self.Channels.stereo
        else:
            sample.channels = self.Channels.mono
        sample.loop_sustain = bool(loop_format_flags & 4)
        sample.panning = data[0x0F] - 0x80
        (sample.relative_note,) = unpack("<b", data[0x10:0x11])
        sample.unknown6 = data[0x11:0x28]

    def load_sample_data(self, chunk):
        index = (chunk.chnm - 2) // 2
        sample = self.samples[index]
        sample.data = chunk.chdt
        format = chunk.chff & 0x07 or 1
        sample.format = self.Format(format)
        if sample.format is None:
            sample.format = self.Format.int8
        sample.channels = self.Channels(chunk.chff & 0x08)
        sample.rate = chunk.chfr

    def finalize_load(self):
        if not self.volume_envelope.loaded:
            self._upgrade_envelopes()

    def _upgrade_envelopes(self):
        log.info(
            _F(
                "Upgrading Sampler{} to infinite envelope format",
                "[{}]".format(self.index) if self.index is not None else "",
            )
        )
        vol = self.volume_envelope
        pan = self.panning_envelope
        vol.bitmask = vol._legacy_bitmask
        vol.sustain_point = vol._legacy_sustain_point
        vol.loop_start_point = vol._legacy_loop_start_point
        vol.loop_end_point = vol._legacy_loop_end_point
        pan.bitmask = pan._legacy_bitmask
        pan.sustain_point = pan._legacy_sustain_point
        pan.loop_start_point = pan._legacy_loop_start_point
        pan.loop_end_point = pan._legacy_loop_end_point
        vol_x_points = [
            unpack("<H", vol._legacy_point_bytes[4 * i : 4 * i + 2])[0]
            for i in range(vol._legacy_active_points)
        ]
        pan_x_points = [
            unpack("<H", pan._legacy_point_bytes[4 * i : 4 * i + 2])[0]
            for i in range(pan._legacy_active_points)
        ]
        vol_y_points = [
            unpack("<H", vol._legacy_point_bytes[4 * i + 2 : 4 * i + 4])[0] * 0x200
            for i in range(vol._legacy_active_points)
        ]
        pan_y_points = [
            unpack("<H", pan._legacy_point_bytes[4 * i + 2 : 4 * i + 4])[0] * 0x200
            - pan.range[0]
            for i in range(pan._legacy_active_points)
        ]
        vol.points = [
            (vol_x_points[i], vol_y_points[i]) for i in range(vol._legacy_active_points)
        ]
        pan.points = [
            (pan_x_points[i], pan_y_points[i]) for i in range(pan._legacy_active_points)
        ]
