# -- DO NOT EDIT THIS FILE DIRECTLY --
"""
Base class for AnalogGenerator
This file was auto-generated by genrv.
"""
from enum import IntEnum

from rv.controller import Controller
from rv.option import Option


class BaseAnalogGenerator:
    name = "AnalogGenerator"
    mtype = "Analog generator"
    mgroup = "Synth"
    flags = 0x49

    class Mode(IntEnum):
        hq = 0
        hq_mono = 1
        lq = 2
        lq_mono = 3

    class Waveform(IntEnum):
        triangle = 0
        saw = 1
        square = 2
        noise = 3
        drawn = 4
        sin = 5
        hsin = 6
        asin = 7
        drawn_spline = 8
        noise_spline = 9
        white_noise = 10
        pink_noise = 11
        red_noise = 12
        blue_noise = 13
        violet_noise = 14
        grey_noise = 15
        harmonics = 16

    class Filter(IntEnum):
        off = 0
        lp_12db = 1
        hp_12db = 2
        bp_12db = 3
        br_12db = 4
        lp_24db = 5
        hp_24db = 6
        bp_24db = 7
        br_24db = 8

    class FilterEnvelope(IntEnum):
        off = 0
        sustain_off = 1
        sustain_on = 2

    class Osc2Mode(IntEnum):
        add = 0
        sub = 1
        mul = 2
        min = 3
        max = 4
        bitwise_and = 5
        bitwise_xor = 6

    volume = Controller((0, 256), 80)
    waveform = Controller(Waveform, Waveform.triangle)
    panning = Controller((-128, 128), 0)
    attack = Controller((0, 256), 0)
    release = Controller((0, 256), 0)
    sustain = Controller(bool, True)
    exponential_envelope = Controller(bool, True)
    duty_cycle = Controller((0, 1024), 512)
    osc2_semitone_64 = Controller((-1000, 1000), 0)
    filter = Controller(Filter, Filter.off)
    f_freq = Controller((0, 14000), 14000)
    f_resonance = Controller((0, 1530), 0)
    f_exponential_freq = Controller(bool, True)
    f_attack = Controller((0, 256), 0)
    f_release = Controller((0, 256), 0)
    f_envelope = Controller(FilterEnvelope, FilterEnvelope.off)
    polyphony = Controller((1, 32), 16)
    mode = Controller(Mode, Mode.hq_mono)
    noise = Controller((0, 256), 0)
    osc2_volume = Controller((0, 32768), 32768)
    osc2_mode = Controller(Osc2Mode, Osc2Mode.add)
    volume_envelope_scaling_per_key = Option(
        name="volume_envelope_scaling_per_key",
        number=127,
        byte=0,
        bit=0,
        size=1,
        default=False,
    )
    filter_envelope_scaling_per_key = Option(
        name="filter_envelope_scaling_per_key",
        number=126,
        byte=1,
        bit=0,
        size=1,
        default=False,
    )
    volume_scaling_per_key = Option(
        name="volume_scaling_per_key", number=125, byte=2, bit=0, size=1, default=False
    )
    filter_freq_scaling_per_key = Option(
        name="filter_freq_scaling_per_key",
        number=124,
        byte=3,
        bit=0,
        size=1,
        default=False,
    )
    filter_freq_scaling_per_key_reverse = Option(
        name="filter_freq_scaling_per_key_reverse",
        number=120,
        byte=7,
        bit=0,
        size=1,
        default=False,
    )
    filter_freq_eq_note_freq = Option(
        name="filter_freq_eq_note_freq",
        number=117,
        byte=10,
        bit=0,
        size=1,
        default=False,
    )
    velocity_dependent_filter_frequency = Option(
        name="velocity_dependent_filter_frequency",
        number=123,
        byte=4,
        bit=0,
        size=1,
        default=False,
    )
    velocity_dependent_filter_resonance = Option(
        name="velocity_dependent_filter_resonance",
        number=116,
        byte=11,
        bit=0,
        size=1,
        default=False,
    )
    frequency_div_2 = Option(
        name="frequency_div_2", number=122, byte=5, bit=0, size=1, default=False
    )
    smooth_frequency_change = Option(
        name="smooth_frequency_change",
        number=121,
        byte=6,
        bit=0,
        size=1,
        inverted=True,
        default=True,
    )
    retain_phase = Option(
        name="retain_phase", number=119, byte=8, bit=0, size=1, default=False
    )
    random_phase = Option(
        name="random_phase", number=118, byte=9, bit=0, size=1, default=False
    )
    true_zero_attack_release = Option(
        name="true_zero_attack_release",
        number=115,
        byte=12,
        bit=0,
        size=1,
        default=False,
    )
