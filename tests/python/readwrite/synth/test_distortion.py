from rv.api import m


def test_distortion(read_write_read_synth):
    mod: m.Distortion = read_write_read_synth("distortion").module
    assert mod.flags == 0x02000051
    assert mod.name == "distortion"
    assert mod.volume == 99
    assert mod.type == mod.Type.foldback2
    assert mod.power == 94
    assert mod.bit_depth == 15
    assert mod.freq == 23609
    assert mod.noise == 196
