from struct import pack

from pytest import raises
from rv.api import m

EXPECTED_DRAWN_WAVEFORM = [
    0,
    -100,
    -90,
    0,
    -35,
    -35,
    -35,
    -35,
    -35,
    -35,
    -35,
    -32,
    -24,
    -17,
    -4,
    12,
    36,
    94,
    77,
    50,
    33,
    27,
    50,
    32,
    -90,
    -120,
    100,
    90,
    59,
    21,
    0,
    54,
]


def test_analog_generator(read_write_read_synth):
    mod: m.AnalogGenerator = read_write_read_synth("analog-generator").module

    assert mod.flags == 0x49
    assert mod.name == "analog-generator"

    assert mod.drawn_waveform.samples == EXPECTED_DRAWN_WAVEFORM

    assert mod.volume == 103
    assert mod.waveform == mod.Waveform.drawn
    assert mod.panning == -19
    assert mod.attack == 91
    assert mod.release == 97
    assert mod.sustain
    assert mod.exponential_envelope
    assert mod.duty_cycle == 534
    assert mod.freq2 == 1393
    assert mod.filter == mod.Filter.bp_12db
    assert mod.f_freq_hz == 5611
    assert mod.f_resonance == 1183
    assert not mod.f_exponential_freq
    assert mod.f_attack == 87
    assert mod.f_release == 58
    assert mod.f_envelope == mod.FilterEnvelope.off
    assert mod.polyphony_ch == 32
    assert mod.mode == mod.Mode.lq
    assert mod.noise == 9
    assert mod.volume_envelope_scaling_per_key
    assert not mod.filter_envelope_scaling_per_key
    assert mod.volume_scaling_per_key
    assert not mod.filter_freq_scaling_per_key
    assert mod.filter_freq_scaling_per_key_reverse
    assert not mod.filter_freq_eq_note_freq
    assert mod.velocity_dependent_filter_frequency
    assert not mod.velocity_dependent_filter_resonance
    assert mod.frequency_div_2
    assert not mod.smooth_frequency_change
    assert mod.retain_phase
    assert not mod.random_phase
    assert mod.true_zero_attack_release


def test_analog_generator_writes_correct_chunks(read_write_read_synth):
    synth = read_write_read_synth("analog-generator")
    chunks = synth.chunks()

    def v():
        return next(chunks)

    def expect_chunk(*chunk):
        assert v() == chunk

    def expect_cval(value):
        expect_chunk(b"CVAL", pack("<i", value))

    expect_chunk(b"SSYN", b"")
    expect_chunk(b"VERS", b"\x02\x05\x09\x01")
    expect_chunk(b"SFFF", b"\x49\0\0\0")
    expect_chunk(b"SNAM", b"analog-generator\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0")
    expect_chunk(b"STYP", b"Analog generator\0")
    expect_chunk(b"SFIN", b"\x01\0\0\0")
    expect_chunk(b"SREL", b"\x02\0\0\0")
    expect_chunk(b"SSCL", b"\xdd\x01\0\0")
    expect_chunk(b"SCOL", b"\xae\xff\0")
    expect_chunk(b"SMII", b"\0\0\0\0")
    expect_chunk(b"SMIC", b"\0\0\0\0")
    expect_chunk(b"SMIB", b"\xff\xff\xff\xff")
    expect_chunk(b"SMIP", b"\xff\xff\xff\xff")

    expect_cval(103)
    expect_cval(4)
    expect_cval(109)
    expect_cval(91)
    expect_cval(97)
    expect_cval(1)
    expect_cval(1)
    expect_cval(534)
    expect_cval(1393)
    expect_cval(3)
    expect_cval(5611)
    expect_cval(1183)
    expect_cval(0)
    expect_cval(87)
    expect_cval(58)
    expect_cval(0)
    expect_cval(32)
    expect_cval(2)
    expect_cval(9)

    expect_chunk(
        b"CMID",
        b"\x03\x01\x01\x00\x02\x00\x00\xc8"
        b"\x00\x00\x00\x00\x00\x00\x00\xff"
        b"\x00\x00\x00\x00\x00\x00\x00\xff"
        b"\x00\x00\x00\x00\x00\x00\x00\xff"
        b"\x00\x00\x00\x00\x00\x00\x00\xff"
        b"\x00\x00\x00\x00\x00\x00\x00\xff"
        b"\x00\x00\x00\x00\x00\x00\x00\xff"
        b"\x00\x00\x00\x00\x00\x00\x00\xff"
        b"\x00\x00\x00\x00\x00\x00\x00\xff"
        b"\x00\x00\x00\x00\x00\x00\x00\xff"
        b"\x00\x00\x00\x00\x00\x00\x00\xff"
        b"\x00\x00\x00\x00\x00\x00\x00\xff"
        b"\x00\x00\x00\x00\x00\x00\x00\xff"
        b"\x00\x00\x00\x00\x00\x00\x00\xff"
        b"\x00\x00\x00\x00\x00\x00\x00\xff"
        b"\x00\x00\x00\x00\x00\x00\x00\xff"
        b"\x00\x00\x00\x00\x00\x00\x00\xff"
        b"\x00\x00\x00\x00\x00\x00\x00\xff"
        b"\x00\x00\x00\x00\x00\x00\x00\xff",
    )

    expect_chunk(b"CHNK", b"\2\0\0\0")

    expect_chunk(b"CHNM", b"\1\0\0\0")
    expect_chunk(
        b"CHDT",
        b"\1\0\1\0\1\1\1\1\1\0\0\0\1\0\0\0"
        b"\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0"
        b"\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0"
        b"\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0",
    )

    expect_chunk(b"CHNM", b"\0\0\0\0")
    expect_chunk(b"CHDT", bytes(y & ((1 << 8) - 1) for y in EXPECTED_DRAWN_WAVEFORM))
    expect_chunk(b"CHFR", pack("<I", 44100))
    expect_chunk(b"SEND", b"")
    with raises(StopIteration):
        expect_chunk(b"", b"")
