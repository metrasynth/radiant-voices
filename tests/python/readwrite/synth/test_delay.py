from rv.api import m


def test_delay(read_write_read_synth):
    mod: m.Delay = read_write_read_synth("delay").module
    assert mod.flags == 1105
    assert mod.name == "d e l a y"
    assert mod.dry == 158
    assert mod.wet == 273
    assert mod.delay_l == 242
    assert mod.delay_r == 43
    assert mod.volume_l == 179
    assert mod.volume_r == 57
    assert mod.channels == mod.Channels.stereo
    assert mod.inverse
    assert mod.delay_unit == mod.DelayUnit.line_2
