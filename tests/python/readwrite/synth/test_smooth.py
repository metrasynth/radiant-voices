from rv.api import m


def test_smooth(read_write_read_synth):
    mod: m.Smooth = read_write_read_synth("smooth").module
    assert mod.flags == 81 | 33554432
    assert mod.name == "Smooth"
    assert mod.rise == 7552
    assert mod.fall == 26636
    assert mod.fall_eq_rise is True
    assert mod.scale == 49
    assert mod.mode == mod.Mode.lp_filter
    assert mod.channels == mod.Channels.stereo
