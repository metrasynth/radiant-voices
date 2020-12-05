from rv.api import m


def test_spectravoice(read_write_read_synth):
    mod: m.SpectraVoice = read_write_read_synth("spectravoice").module

    assert mod.flags == 0x49
    assert mod.name == "SpectraVoice"

    assert mod.harmonic_freqs.values == EXPECTED_HARMONIC_FREQS
    assert mod.harmonic_volumes.values == EXPECTED_HARMONIC_VOLUMES
    assert mod.harmonic_widths.values == EXPECTED_HARMONIC_WIDTHS
    assert mod.harmonic_types.values == EXPECTED_HARMONIC_TYPES

    assert mod.volume == 219
    assert mod.panning == -77
    assert mod.attack == 234
    assert mod.release == 324
    assert mod.polyphony_ch == 21
    assert mod.mode == mod.Mode.lq_mono
    assert not mod.sustain
    assert mod.spectrum_resolution == 4
    assert mod.harmonic == 10
    assert mod.h_freq_hz == 14729
    assert mod.h_volume == 224
    assert mod.h_width == 94
    assert mod.h_type == mod.HarmonicType.overtones2


EXPECTED_HARMONIC_FREQS = [
    17916,
    7063,
    5426,
    7235,
    18002,
    10594,
    775,
    20586,
    10853,
    16279,
    14729,
    4479,
    12231,
    3876,
    19036,
    21275,
]


EXPECTED_HARMONIC_VOLUMES = [
    114,
    203,
    245,
    42,
    191,
    102,
    243,
    195,
    184,
    59,
    224,
    144,
    213,
    182,
    21,
    238,
]

EXPECTED_HARMONIC_WIDTHS = [
    99,
    242,
    70,
    26,
    245,
    9,
    43,
    10,
    219,
    135,
    94,
    235,
    66,
    124,
    114,
    16,
]

EXPECTED_HARMONIC_TYPES = [
    m.SpectraVoice.HarmonicType.org2,
    m.SpectraVoice.HarmonicType.rect,
    m.SpectraVoice.HarmonicType.overtones4,
    m.SpectraVoice.HarmonicType.sin,
    m.SpectraVoice.HarmonicType.overtones4,
    m.SpectraVoice.HarmonicType.overtones4,
    m.SpectraVoice.HarmonicType.triangle1,
    m.SpectraVoice.HarmonicType.overtones1,
    m.SpectraVoice.HarmonicType.org4,
    m.SpectraVoice.HarmonicType.rect,
    m.SpectraVoice.HarmonicType.overtones2,
    m.SpectraVoice.HarmonicType.overtones3,
    m.SpectraVoice.HarmonicType.org4,
    m.SpectraVoice.HarmonicType.overtones4,
    m.SpectraVoice.HarmonicType.org1,
    m.SpectraVoice.HarmonicType.overtones1,
]
