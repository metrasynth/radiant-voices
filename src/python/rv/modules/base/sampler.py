# -- DO NOT EDIT THIS FILE DIRECTLY --
"""
Base class for Sampler
This file was auto-generated by genrv.
"""
from enum import IntEnum

from rv.controller import Controller
from rv.option import Option


class BaseSampler:
    name = "Sampler"
    mtype = "Sampler"
    mgroup = "Synth"
    flags = 0x2008459

    class SampleInterpolation(IntEnum):
        off = 0
        linear = 1
        spline = 2

    class EnvelopeInterpolation(IntEnum):
        off = 0
        linear = 1

    class VibratoType(IntEnum):
        sin = 0
        saw = 1
        square = 2

    class LoopType(IntEnum):
        off = 0
        forward = 1
        ping_pong = 2

    class Format(IntEnum):
        int8 = 1
        int16 = 2
        float32 = 4

    class Channels(IntEnum):
        mono = 0
        stereo = 8

    class EnvelopeFlags(IntEnum):
        enabled = 1
        sustain = 2
        loop = 4

    volume = Controller((0, 512), 256)
    panning = Controller((-128, 128), 0)
    sample_interpolation = Controller(SampleInterpolation, SampleInterpolation.spline)
    envelope_interpolation = Controller(
        EnvelopeInterpolation, EnvelopeInterpolation.linear
    )
    polyphony = Controller((1, 32), 8)
    rec_threshold = Controller((0, 10000), 4)
    start_recording_on_project_play = Option(
        name="start_recording_on_project_play",
        number=127,
        byte=0,
        bit=0,
        size=1,
        default=False,
    )
    stop_recording_on_project_stop = Option(
        name="stop_recording_on_project_stop",
        number=123,
        byte=4,
        bit=0,
        size=1,
        default=False,
    )
    record_in_mono = Option(
        name="record_in_mono",
        number=126,
        byte=1,
        bit=0,
        size=1,
        default=False,
    )
    record_with_reduced_sample_rate = Option(
        name="record_with_reduced_sample_rate",
        number=125,
        byte=2,
        bit=0,
        size=1,
        default=False,
    )
    record_in_16_bit = Option(
        name="record_in_16_bit",
        number=124,
        byte=3,
        bit=0,
        size=1,
        default=False,
    )
    ignore_velocity_for_volume = Option(
        name="ignore_velocity_for_volume",
        number=122,
        byte=5,
        bit=0,
        size=1,
        default=False,
    )
    increased_freq_computation_accuracy = Option(
        name="increased_freq_computation_accuracy",
        number=121,
        byte=6,
        bit=0,
        size=1,
        default=False,
    )
