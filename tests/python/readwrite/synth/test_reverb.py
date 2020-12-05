from rv.api import m


def test_reverb(read_write_read_synth):
    mod: m.Reverb = read_write_read_synth("reverb").module
    assert mod.flags == 81
    assert mod.name == "Reverb"
    assert mod.dry == 140
    assert mod.wet == 134
    assert mod.feedback == 146
    assert mod.damp == 0
    assert mod.stereo_width == 75
    assert mod.freeze
    assert mod.mode == mod.Mode.lq
    assert mod.all_pass_filter
    assert mod.room_size == 32
    assert mod.random_seed == 23552
