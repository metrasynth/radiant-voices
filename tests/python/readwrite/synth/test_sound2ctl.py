from rv.api import m


def test_sound2ctl(read_write_read_synth):
    mod: m.Sound2Ctl = read_write_read_synth("sound2ctl").module
    assert mod.flags == 393297
    assert mod.name == "Sound2Ctl"
    assert mod.sample_rate_hz == 14687
    assert not mod.absolute
    assert mod.gain == 741
    assert mod.smooth == 24
    assert mod.mode == mod.Mode.lq
    assert mod.out_min == 12054
    assert mod.out_max == 21842
    assert mod.out_controller == 223
