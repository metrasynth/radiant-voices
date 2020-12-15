from rv.api import m


def test_echo(read_write_read_synth):
    mod: m.Echo = read_write_read_synth("echo").module
    assert mod.flags == 1105
    assert mod.name == "echo"
    assert mod.dry == 80
    assert mod.wet == 88
    assert mod.feedback == 234
    assert mod.delay == 133
    assert mod.channels == mod.Channels.mono
    assert mod.delay_unit == mod.DelayUnit.line
