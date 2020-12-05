from rv.api import m


def test_kicker(read_write_read_synth):
    mod: m.Kicker = read_write_read_synth("kicker").module
    assert mod.flags == 73
    assert mod.name == "kickadee"
    assert mod.volume == 137
    assert mod.waveform == mod.Waveform.triangle
    assert mod.panning == 37
    assert mod.attack == 392
    assert mod.release == 399
    assert mod.boost == 842
    assert mod.acceleration == 155
    assert mod.polyphony_ch == 1
    assert not mod.no_click
