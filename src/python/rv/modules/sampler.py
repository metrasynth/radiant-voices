import logging
from io import BytesIO
from itertools import chain
from struct import pack, unpack
from typing import BinaryIO, List, Optional

from logutils import BraceMessage as _F
from rv.chunks.chunk import Chunk
from rv.controller import Controller
from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.sampler import BaseSampler
from rv.note import NOTE
from rv.readers.reader import read_sunvox_file
from rv.synth import Synth

log = logging.getLogger(__name__)


class Sampler(BaseSampler, Module):
    INS_SIGN = b"PMAS"  # "SAMP" in little-endian
    INS_VERSION = 6
    XI_ENV_POINTS = 12

    chnk = 0x010B
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
                data += pack("<HH", x, y - self.range[0])
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
            self._length = 0
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
            self.reserved2 = 0
            self.name = b""
            self.start_pos = 0

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
    version: int
    max_version: int

    # Legacy
    instrument_name: bytes
    volume_old: int
    ins_finetune: int
    ins_relative_note: int
    editor_cursor: int
    editor_selected_size: int

    # Unused
    unused1: int
    unused2: int
    unused3: int
    unused4: int
    unused5: int
    unused6: int

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
        self.instrument_name = kwargs.get("instrument_name", b"")
        self.version = self.INS_VERSION
        self.max_version = self.INS_VERSION
        self.unused1 = 0
        self.unused2 = 0
        self.unused3 = 0
        self.unused4 = 0
        self.unused5 = 0
        self.unused6 = 0
        self.volume_old = 64
        self.ins_finetune = 0
        self.ins_relative_note = 0
        self.editor_cursor = 0
        self.editor_selected_size = 0
        self.effect = None
        # Special handling for legacy instruments.
        # Starts out as an empty list, then populated with raw chunks during load.
        # If the INS_SIGN signature is not found, the `is_legacy` flag is set True.
        # If it is found, it is set False and `legacy_chunks` is cleared.
        # When writing out, if this is None then new chunks are written.
        # If it is a list, then raw chunks are written out instead.
        # This can go away once we better support legacy instruments.
        self.is_legacy: bool | None = None
        self.legacy_chunks: list[Chunk] | None = []

    def specialized_iff_chunks(self):
        if self.is_legacy:
            for chunk in self.legacy_chunks:
                yield from chunk.chunks()
            return
        iters = [
            self.global_config_chunks(),  # CHNM 0x0000
            self.sample_data_chunks(),  # CHNM i*2+1, i*2+2
            super(Sampler, self).specialized_iff_chunks(),  # CHNM 0x0101
            self.volume_envelope.chunks(),  # CHNM 0x0102
            self.panning_envelope.chunks(),  # CHNM 0x0103
            self.pitch_envelope.chunks(),  # CHNM 0x0104
            self.effect_control_envelopes[0].chunks(),  # CHNM 0x0105
            self.effect_control_envelopes[1].chunks(),  # CHNM 0x0106
            self.effect_control_envelopes[2].chunks(),  # CHNM 0x0107
            self.effect_control_envelopes[3].chunks(),  # CHNM 0x0108
        ]
        for iter in iters:
            yield from iter
        if self.effect:  # CHNM 0x010a
            f = BytesIO()
            self.effect.write_to(f)
            yield b"CHNM", b"\x0a\x01\0\0"
            yield b"CHDT", f.getvalue()

    def sample_data_chunks(self):
        for i, sample in enumerate(self.samples):
            if sample is not None:
                yield from self.sample_chunks(i, sample)

    def global_config_chunks(self):
        f = BytesIO()
        w = _StructWriter(f)

        vol = self.volume_envelope
        pan = self.panning_envelope

        # uint32_t unused1;
        w.uint32(self.unused1)
        # char name[ 22 ];
        w.char(self.instrument_name, 22)
        # uint16_t unused2;
        w.uint16(self.unused2)
        # uint16_t samples_num;
        compacted_samples = self.samples.copy()
        while compacted_samples and compacted_samples[-1] is None:
            compacted_samples.pop()
        w.uint16(len(compacted_samples))
        # uint16_t unused3;
        w.uint16(self.unused3)
        # uint32_t unused4;
        w.uint32(self.unused4)
        # uint8_t smp_num_old[ 96 ];
        f.write(self.note_samples.bytes[:96])
        # uint16_t volume_points_old[ XI_ENV_POINTS * 2 ];
        f.write(vol.point_bytes)
        # uint16_t panning_points_old[ XI_ENV_POINTS * 2 ];
        f.write(pan.point_bytes)
        # uint8_t volume_points_num_old;
        w.uint8(len(vol.points))
        # uint8_t panning_points_num_old;
        w.uint8(len(pan.points))
        # uint8_t vol_sustain_old;
        w.uint8(vol.sustain_point)
        # uint8_t vol_loop_start_old;
        w.uint8(vol.loop_start_point)
        # uint8_t vol_loop_end_old;
        w.uint8(vol.loop_end_point)
        # uint8_t pan_sustain_old;
        w.uint8(pan.sustain_point)
        # uint8_t pan_loop_start_old;
        w.uint8(pan.loop_start_point)
        # uint8_t pan_loop_end_old;
        w.uint8(pan.loop_end_point)
        # uint8_t volume_type_old;
        w.uint8(vol.bitmask)
        # uint8_t panning_type_old;
        w.uint8(pan.bitmask)
        # uint8_t vibrato_type;
        w.uint8(self.vibrato_type.value)
        # uint8_t vibrato_sweep;
        w.uint8(self.vibrato_attack)
        # uint8_t vibrato_depth;
        w.uint8(self.vibrato_depth)
        # uint8_t vibrato_rate;
        w.uint8(self.vibrato_rate)
        # uint16_t volume_fadeout;
        w.uint16(self.volume_fadeout)
        # uint8_t volume_old;
        w.uint8(self.volume_old)
        # int8_t finetune;
        w.int8(self.ins_finetune)
        # uint8_t unused5;
        w.uint8(self.unused5)
        # int8_t relative_note;
        w.int8(self.ins_relative_note)
        # uint32_t unused6;
        w.uint32(self.unused6)
        # uint32_t sign;
        f.write(self.INS_SIGN)  # "SAMP" in little-endian
        # uint32_t version;
        w.uint32(self.version)
        # uint8_t smp_num[ 128 ];
        f.write(self.note_samples.bytes)
        # uint32_t max_version;
        w.uint32(self.max_version)
        # int32_t editor_cursor;
        w.int32(self.editor_cursor)
        # int32_t editor_selected_size;
        w.int32(self.editor_selected_size)

        yield b"CHNM", pack("<I", 0)
        yield b"CHDT", f.getvalue()
        f.close()

    def envelope_config_chunks(self):
        yield b"CHNM", pack("<I", 0x101)
        yield b"CHDT", b"\x00\x00\x00\x00\x00\x00"

    def sample_chunks(self, i, sample):
        f = BytesIO()
        w = _StructWriter(f)

        # uint32_t length;
        w.uint32(sample.frames)
        # uint32_t reppnt;
        w.uint32(sample.loop_start)
        # uint32_t replen;
        w.uint32(sample.loop_len)
        # uint8_t volume;
        w.uint8(sample.volume)
        # int8_t finetune;
        w.int8(sample.finetune)
        # uint8_t type;
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
        w.uint8(loop_format_flags)
        # uint8_t panning;
        w.uint8(sample.panning + 0x80)
        # int8_t relative_note;
        w.int8(sample.relative_note)
        # uint8_t reserved2;
        w.uint8(sample.reserved2)
        # char name[ 22 ];
        w.char(sample.name, 22)
        # uint32_t start_pos;
        w.uint32(sample.start_pos)

        yield b"CHNM", pack("<I", i * 2 + 1)
        yield b"CHDT", f.getvalue()
        f.close()
        yield b"CHNM", pack("<I", i * 2 + 2)
        yield b"CHDT", sample.data
        yield b"CHFF", pack("<I", sample.format.value | sample.channels.value)
        yield b"CHFR", pack("<I", sample.rate)

    def load_chunk(self, chunk):
        if self.is_legacy is not False:
            self.legacy_chunks.append(chunk)
        chnm = chunk.chnm
        chdt = chunk.chdt
        if chnm == self.options_chnm:
            self.load_options(chunk)
        elif chnm == 0:
            self.load_instrument(chunk)
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

    def load_instrument(self, chunk):
        data = chunk.chdt
        r = _StructReader(data)

        vol = self.volume_envelope
        pan = self.panning_envelope

        # $0000 uint32_t unused1;
        self.unused1 = r.uint32()
        # $0004 char name[ 22 ];
        self.instrument_name = r.char(22)
        # $001a uint16_t unused2;
        self.unused2 = r.uint16()
        # $001c uint16_t samples_num;
        _ = r.uint16()
        # $001e uint16_t unused3;
        self.unused3 = r.uint16()
        # $0020 uint32_t unused4;
        self.unused4 = r.uint32()
        # $0024 uint8_t smp_num_old[ 96 ];
        self.note_samples.bytes = r.bytes(96)
        # $0084 uint16_t volume_points_old[ XI_ENV_POINTS * 2 ];
        vol._legacy_point_bytes = r.bytes(self.XI_ENV_POINTS * 2 * 2)
        # $0086 uint16_t panning_points_old[ XI_ENV_POINTS * 2 ];
        pan._legacy_point_bytes = r.bytes(self.XI_ENV_POINTS * 2 * 2)
        # $0088 uint8_t volume_points_num_old;
        vol._legacy_active_points = r.uint8()
        # $0089 uint8_t panning_points_num_old;
        pan._legacy_active_points = r.uint8()
        # $008a uint8_t vol_sustain_old;
        vol._legacy_sustain_point = r.uint8()
        # $008b uint8_t vol_loop_start_old;
        vol._legacy_loop_start_point = r.uint8()
        # $008c uint8_t vol_loop_end_old;
        vol._legacy_loop_end_point = r.uint8()
        # $008d uint8_t pan_sustain_old;
        pan._legacy_sustain_point = r.uint8()
        # $008e uint8_t pan_loop_start_old;
        pan._legacy_loop_start_point = r.uint8()
        # $008f uint8_t pan_loop_end_old;
        pan._legacy_loop_end_point = r.uint8()
        # $0090 uint8_t volume_type_old;
        vol._legacy_bitmask = r.uint8()
        # $0091 uint8_t panning_type_old;
        pan._legacy_bitmask = r.uint8()
        # $0092 uint8_t vibrato_type;
        self.vibrato_type = self.VibratoType(r.uint8())
        # $0093 uint8_t vibrato_sweep;
        self.vibrato_attack = r.uint8()
        # $0094 uint8_t vibrato_depth;
        self.vibrato_depth = r.uint8()
        # $0095 uint8_t vibrato_rate;
        self.vibrato_rate = r.uint8()
        # $0096 uint16_t volume_fadeout;
        self.volume_fadeout = r.uint16()
        # $0098 uint8_t volume_old;
        self.volume_old = r.uint8()
        # $0099 int8_t finetune;
        self.ins_finetune = r.int8()
        # $009a uint8_t unused5;
        self.unused5 = r.uint8()
        # $009b int8_t relative_note;
        self.ins_relative_note = r.int8()
        # $009c uint32_t unused6;
        self.unused6 = r.uint32()
        # $00a0 uint32_t sign;
        sign = r.char(4)
        if sign != self.INS_SIGN:
            log.warning("legacy signature %r != %r", sign, self.INS_SIGN)
            self.is_legacy = True
        # $00a4 uint32_t version;
        self.version = r.uint32()
        # $00a8 uint8_t smp_num[ 128 ];
        self.note_samples.bytes = r.char(128)
        # $0128 uint32_t max_version;
        self.max_version = r.uint32(self.INS_VERSION)
        # $012b int32_t editor_cursor;
        self.editor_cursor = r.int32(0)
        # $012f int32_t editor_selected_size;
        self.editor_selected_size = r.int32(0)

        if not self.is_legacy and len(data) >= 0x190:
            log.warning(f"legacy instrument data of length {len(data)}")
            self.is_legacy = True
        if not self.is_legacy:
            self.is_legacy = False
            self.legacy_chunks = None

    def load_sample_meta(self, chunk):
        index = (chunk.chnm - 1) // 2
        sample = self.samples[index] = self.Sample()
        data = chunk.chdt

        r = _StructReader(data)

        # uint32_t length;
        sample._length = r.uint32()
        # uint32_t reppnt;
        sample.loop_start = r.uint32()
        # uint32_t replen;
        sample.loop_len = r.uint32()
        # uint8_t volume;
        sample.volume = r.uint8()
        # int8_t finetune;
        sample.finetune = r.int8()
        # uint8_t type;
        loop_format_flags = r.uint8()
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
        # uint8_t panning;
        sample.panning = r.uint8() - 0x80
        # int8_t relative_note;
        sample.relative_note = r.int8()
        # uint8_t reserved2;
        sample.reserved2 = r.uint8()
        # char name[ 22 ];
        sample.name = r.char(22)
        # uint32_t start_pos;
        sample.start_pos = r.uint32(0)

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
            + vol.range[0]
            for i in range(vol._legacy_active_points)
        ]
        pan_y_points = [
            unpack("<H", pan._legacy_point_bytes[4 * i + 2 : 4 * i + 4])[0] * 0x200
            + pan.range[0]
            for i in range(pan._legacy_active_points)
        ]
        vol.points = [
            (vol_x_points[i], vol_y_points[i]) for i in range(vol._legacy_active_points)
        ]
        pan.points = [
            (pan_x_points[i], pan_y_points[i]) for i in range(pan._legacy_active_points)
        ]


class _StructWriter:
    def __init__(self, f: BinaryIO):
        self._f = f

    def char(self, value: bytes, width: int) -> None:
        self._f.write(value.ljust(width, b"\0")[:width])

    def int8(self, value: int) -> None:
        self._f.write(pack("<b", value))

    def uint8(self, value: int) -> None:
        self._f.write(pack("<B", value))

    def int16(self, value: int) -> None:
        self._f.write(pack("<h", value))

    def uint16(self, value: int) -> None:
        self._f.write(pack("<H", value))

    def int32(self, value: int) -> None:
        self._f.write(pack("<i", value))

    def uint32(self, value: int) -> None:
        self._f.write(pack("<I", value))


class _StructReader:
    def __init__(self, data: bytes):
        self._data = data
        self._index = 0

    def bytes(self, length: int) -> bytes:
        start = self._index
        new_index = start + length
        buf = self._data[start:new_index]
        self._index = new_index
        return buf

    def char(self, length: int) -> bytes:
        return self.bytes(length).rstrip(b"\0")

    def skip(self, length: int) -> None:
        self._index += length

    def int8(self, default=None) -> int:
        return self._read("<b", 1, default)

    def uint8(self, default=None) -> int:
        return self._read("<B", 1, default)

    def int16(self, default=None) -> int:
        return self._read("<h", 2, default)

    def uint16(self, default=None) -> int:
        return self._read("<H", 2, default)

    def int32(self, default=None) -> int:
        return self._read("<i", 4, default)

    def uint32(self, default=None) -> int:
        return self._read("<I", 4, default)

    def _read(self, spec: str, length: int, default=None) -> int:
        start = self._index
        new_index = start + length
        buf = self._data[start:new_index]
        if len(buf) < length:
            if default is None:
                raise RuntimeError("default not provided")
            return default
        self._index = new_index
        return unpack(spec, buf)[0]
