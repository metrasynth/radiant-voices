from rv.api import m

EXPECTED_DRAWN_WAVEFORM = [
    0,
    -100,
    -90,
    0,
    90,
    -119,
    -55,
    -38,
    6,
    44,
    68,
    68,
    52,
    19,
    -31,
    -49,
    -58,
    -58,
    -50,
    -25,
    38,
    58,
    58,
    58,
    -90,
    -120,
    100,
    90,
    59,
    21,
    0,
    54,
]


def test_generator(read_write_read_synth):
    mod: m.Generator = read_write_read_synth("generator").module
    assert mod.flags == 0x59
    assert mod.name == "gen"

    assert mod.drawn_waveform.samples == EXPECTED_DRAWN_WAVEFORM

    assert mod.volume == 136
    assert mod.waveform == mod.Waveform.drawn
    assert mod.panning == -85
    assert mod.attack == 359
    assert mod.release == 115
    assert mod.polyphony_ch == 6
    assert mod.mode == mod.Mode.mono
    assert mod.sustain
    assert mod.freq_modulation_by_input == 99
    assert mod.duty_cycle == 283
