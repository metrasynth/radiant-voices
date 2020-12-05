from struct import pack

from rv.api import NOTE, m


def test_sampler(read_write_read_synth):
    mod: m.Sampler = read_write_read_synth("sampler").module

    assert mod.flags == 33881
    assert mod.name == "Sampler"

    assert mod.volume == 267
    assert mod.panning == 50
    assert mod.sample_interpolation == mod.SampleInterpolation.linear
    assert mod.envelope_interpolation == mod.EnvelopeInterpolation.off
    assert mod.polyphony_ch == 32
    assert mod.rec_threshold == 2448

    # Global sampler config
    assert mod.vibrato_type == mod.VibratoType.square
    assert mod.vibrato_attack == 50
    assert mod.vibrato_depth == 118
    assert mod.vibrato_rate == 11
    assert mod.volume_fadeout == 3696

    vol_env = mod.volume_envelope
    assert vol_env.enable
    assert vol_env.sustain
    assert not vol_env.loop
    assert vol_env.ctl_index == 0
    assert vol_env.gain_pct == 64
    assert vol_env.velocity == 32
    assert vol_env.sustain_point == 0
    assert vol_env.loop_start_point == 0
    assert vol_env.loop_end_point == 0
    assert vol_env.points == [
        (0, 32768),
        (33, 9728),
        (98, 14848),
        (133, 4096),
        (256, 0),
    ]

    panning_env = mod.panning_envelope
    assert not panning_env.enable
    assert not panning_env.sustain
    assert not panning_env.loop
    assert panning_env.ctl_index == 0
    assert panning_env.gain_pct == 82
    assert panning_env.velocity == 28
    assert panning_env.sustain_point == 0
    assert panning_env.loop_start_point == 0
    assert panning_env.loop_end_point == 0
    assert panning_env.points == [
        (0, 0),
        (36, -4096),
        (68, 4096),
        (115, 9728),
    ]

    pitch_env = mod.pitch_envelope
    assert not pitch_env.enable
    assert not pitch_env.sustain
    assert not pitch_env.loop
    assert pitch_env.gain_pct == 53
    assert pitch_env.velocity == 83
    assert pitch_env.sustain_point == 0
    assert pitch_env.loop_start_point == 0
    assert pitch_env.loop_end_point == 0
    assert pitch_env.points == [
        (0, 3072),
        (33, -6144),
        (190, 9216),
    ]

    effect_env_1 = mod.effect_control_envelopes[0]
    assert effect_env_1.enable
    assert not effect_env_1.sustain
    assert effect_env_1.loop
    assert effect_env_1.ctl_index == 0
    assert effect_env_1.gain_pct == 69
    assert effect_env_1.velocity == 32
    assert effect_env_1.sustain_point == 0
    assert effect_env_1.loop_start_point == 1
    assert effect_env_1.loop_end_point == 2
    assert effect_env_1.points == [
        (0, 32768),
        (23, 28160),
        (52, 25088),
        (64, 32768),
    ]

    effect_env_2 = mod.effect_control_envelopes[1]
    assert effect_env_2.enable
    assert not effect_env_2.sustain
    assert not effect_env_2.loop
    assert effect_env_2.ctl_index == 1
    assert effect_env_2.gain_pct == 30
    assert effect_env_2.velocity == 83
    assert effect_env_2.sustain_point == 0
    assert effect_env_2.loop_start_point == 0
    assert effect_env_2.loop_end_point == 0
    assert effect_env_2.points == [
        (0, 23040),
        (88, 29696),
    ]

    effect_env_3 = mod.effect_control_envelopes[2]
    assert effect_env_3.enable
    assert not effect_env_3.sustain
    assert not effect_env_3.loop
    assert effect_env_3.ctl_index == 2
    assert effect_env_3.gain_pct == 28
    assert effect_env_3.velocity == 74
    assert effect_env_3.sustain_point == 0
    assert effect_env_3.loop_start_point == 0
    assert effect_env_3.loop_end_point == 0
    assert effect_env_3.points == [
        (0, 15360),
        (178, 31232),
    ]

    effect_env_4 = mod.effect_control_envelopes[3]
    assert not effect_env_4.enable
    assert not effect_env_4.sustain
    assert not effect_env_4.loop
    assert effect_env_4.ctl_index == 3
    assert effect_env_4.gain_pct == 70
    assert effect_env_4.velocity == 58
    assert effect_env_4.sustain_point == 0
    assert effect_env_4.loop_start_point == 0
    assert effect_env_4.loop_end_point == 0
    assert effect_env_4.points == [
        (0, 5632),
        (191, 11264),
    ]

    # Effect
    assert isinstance(mod.effect.module, m.Reverb)

    # <note>:<sample> map
    assert mod.note_samples[NOTE.C4 - 1] == 0
    assert mod.note_samples[NOTE.G4 - 1] == 1
    assert mod.note_samples[NOTE.G5 - 1] == 2

    # Samples
    sample1 = mod.samples[0]
    sample2 = mod.samples[1]
    sample3 = mod.samples[2]

    assert sample1
    assert sample1.frames == 32
    assert sample1.loop_start == 8
    assert sample1.loop_len == 13
    assert sample1.loop_type == mod.LoopType.forward
    assert sample1.volume == 44
    assert sample1.finetune == 72
    assert sample1.panning == 58
    assert sample1.relative_note == 28
    assert sample1.data == pack(
        "<" + ("b" * len(EXPECTED_SAMPLE1_SAMPLES)),
        *EXPECTED_SAMPLE1_SAMPLES,
    )

    assert sample2
    assert sample2.frames == 32
    assert sample2.loop_start == 0
    assert sample2.loop_len == 0
    assert sample2.loop_type == mod.LoopType.off
    assert sample2.volume == 49
    assert sample2.finetune == 78
    assert sample2.panning == -27
    assert sample2.relative_note == -16
    assert sample2.data == pack(
        "<" + ("h" * len(EXPECTED_SAMPLE2_SAMPLES)),
        *EXPECTED_SAMPLE2_SAMPLES,
    )

    assert sample3
    assert sample3.frames == 16
    assert sample3.loop_start == 8
    assert sample3.loop_len == 1
    assert sample3.loop_type == mod.LoopType.ping_pong
    assert sample3.volume == 46
    assert sample3.finetune == -49
    assert sample3.panning == 37
    assert sample3.relative_note == 8
    assert sample3.data == pack(
        "<" + ("f" * len(EXPECTED_SAMPLE3_SAMPLES)),
        *EXPECTED_SAMPLE3_SAMPLES,
    )


EXPECTED_SAMPLE1_SAMPLES = [
    43,
    42,
    40,
    37,
    14,
    -1,
    -8,
    -16,
    -24,
    -29,
    -4,
    14,
    22,
    20,
    10,
    -3,
    -11,
    -17,
    -21,
    -24,
    -25,
    -25,
    -25,
    -22,
    -18,
    -13,
    -9,
    -8,
    -10,
    -13,
    -17,
    -19,
]

EXPECTED_SAMPLE2_SAMPLES = [
    -9088,
    -8960,
    -8960,
    -8896,
    -9152,
    -11648,
    -14656,
    -16256,
    -16256,
    -15808,
    -15040,
    -14336,
    -13504,
    -13120,
    -11584,
    -10944,
    -4992,
    5504,
    13056,
    21184,
    27008,
    28096,
    25664,
    23040,
    20992,
    17984,
    16000,
    14400,
    12992,
    11968,
    11136,
    10432,
]

EXPECTED_SAMPLE3_SAMPLES = [
    -0.310546875,
    0.66015625,
    -0.234375,
    0.6640625,
    -0.177734375,
    0.65234375,
    -0.103515625,
    0.591796875,
    -0.01171875,
    0.515625,
    0.052734375,
    0.333984375,
    0.123046875,
    0.166015625,
    0.1875,
    0.017578125,
    0.271484375,
    -0.103515625,
    0.333984375,
    -0.16796875,
    0.40625,
    -0.2421875,
    0.458984375,
    -0.294921875,
    0.498046875,
    -0.330078125,
    0.515625,
    -0.3515625,
    0.515625,
    -0.37890625,
    0.515625,
    -0.396484375,
]
