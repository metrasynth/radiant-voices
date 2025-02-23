from rv.api import m


def test_glide(read_write_read_synth):
    mod: m.Glide = read_write_read_synth("glide").module
    assert mod.flags == 33951817
    assert mod.name == "Glide"
    assert mod.response == 220
    assert mod.sample_rate == 8676
    assert mod.reset_on_first_note is False
    assert mod.polyphony
    assert mod.pitch == -537
    assert mod.pitch_scale == 48
    assert mod.reset is False
    assert mod.octave == 3
    assert mod.freq_multiply == 5
    assert mod.freq_divide == 7
