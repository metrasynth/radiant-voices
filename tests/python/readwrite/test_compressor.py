from rv.api import m


def test_compressor(read_write_read_sunsynth):
    mod: m.Compressor = read_write_read_sunsynth("compressor").module
    assert mod.flags == 8273
    assert mod.name == "compy"
    assert mod.volume == 442
    assert mod.threshold == 465
    assert mod.slope_pct == 61
    assert mod.attack_ms == 62
    assert mod.release_ms == 925
    assert mod.mode == mod.Mode.peak
    assert mod.sidechain_input == 32
