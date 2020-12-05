from rv.api import m


def test_loop(read_write_read_synth):
    mod: m.Loop = read_write_read_synth("loop").module
    assert mod.flags == 1105
    assert mod.name == "Loop"
    assert mod.volume == 200
    assert mod.delay == 110
    assert mod.channels == mod.Channels.mono
    assert mod.repeats == 35
    assert mod.mode == mod.Mode.normal
