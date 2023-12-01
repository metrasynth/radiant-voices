from rv.api import m


def test_echo(read_write_read_synth):
    mod: m.Echo = read_write_read_synth("echo").module
    assert mod.flags == 0x02000451
    assert mod.name == "echo"
    assert mod.dry == 80
    assert mod.wet == 88
    assert mod.feedback == 234
    assert mod.delay == 133
    assert mod.right_channel_offset is True
    assert mod.delay_unit == mod.DelayUnit.line
    assert mod.right_channel_offset_length == 25648
    assert mod.filter == mod.Filter.lp_6db
    assert mod.filter_freq == 6373
