from rv.api import m


def test_amplifier(read_write_read_synth):
    mod: m.Amplifier = read_write_read_synth("amplifier").module
    assert mod.flags == 81
    assert mod.name == "amp"
    assert mod.volume == 378
    assert mod.balance == -63
    assert mod.dc_offset == -33
    assert mod.inverse
    assert mod.stereo_width == 44
    assert not mod.absolute
    assert mod.fine_volume == 21087
    assert mod.gain == 3948
