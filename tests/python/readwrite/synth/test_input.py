from rv.api import m


def test_input(read_write_read_synth):
    mod: m.Input = read_write_read_synth("input").module
    assert mod.flags == 73
    assert mod.name == "inp"
    assert mod.volume == 376
    assert mod.channels == mod.Channels.stereo
