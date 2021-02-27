from rv.api import m


def test_eq(read_write_read_synth):
    mod: m.Eq = read_write_read_synth("eq").module
    assert mod.flags == 81
    assert mod.name == "EQ"
    assert mod.low == 402
    assert mod.middle == 476
    assert mod.high == 445
    assert mod.channels == mod.Channels.mono
