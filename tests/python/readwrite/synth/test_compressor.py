from rv.api import m


def test_compressor(read_write_read_synth):
    mod: m.Compressor = read_write_read_synth("compressor").module
    assert mod.flags == 0x02002051
    assert mod.name == "compy"
    assert mod.volume == 442
    assert mod.threshold == 465
    assert mod.slope == 61
    assert mod.attack == 62
    assert mod.release == 925
    assert mod.mode == mod.Mode.peak
    assert mod.sidechain_input == 32
