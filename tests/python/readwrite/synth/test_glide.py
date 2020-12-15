from rv.api import m


def test_glide(read_write_read_synth):
    mod: m.Glide = read_write_read_synth("glide").module
    assert mod.flags == 135241
    assert mod.name == "Glide"
    assert mod.response == 220
    assert mod.sample_rate_hz == 8676
    assert not mod.reset_on_first_note
    assert mod.polyphony
    assert mod.pitch == -537
    assert mod.pitch_scale == 48
    assert not mod.reset
