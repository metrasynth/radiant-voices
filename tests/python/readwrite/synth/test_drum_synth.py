from rv.api import m


def test_drum_synth(read_write_read_synth):
    mod: m.DrumSynth = read_write_read_synth("drum-synth").module
    assert mod.flags == 73
    assert mod.name == "drums"
    assert mod.volume == 255
    assert mod.panning == 1
    assert mod.bass_volume == 201
    assert mod.bass_power == 255
    assert mod.bass_tone == 65
    assert mod.bass_length == 63
    assert mod.hihat_volume == 257
    assert mod.hihat_length == 63
    assert mod.snare_volume == 257
    assert mod.snare_tone == 127
    assert mod.snare_length == 65
    assert mod.bass_panning == -1
    assert mod.hihat_panning == 1
    assert mod.snare_panning == -1
