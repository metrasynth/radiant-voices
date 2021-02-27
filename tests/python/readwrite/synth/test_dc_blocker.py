from rv.api import m


def test_dc_blocker(read_write_read_synth):
    mod: m.DcBlocker = read_write_read_synth("dc-blocker").module
    assert mod.flags == 81
    assert mod.name == "dcb"
    assert mod.channels == mod.Channels.mono
