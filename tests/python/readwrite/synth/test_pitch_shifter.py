from rv.api import m


def test_pitch_shifter(read_write_read_synth):
    mod: m.PitchShifter = read_write_read_synth("pitch-shifter").module
    assert mod.flags == 81
    assert mod.name == "Pitch shifter"
    assert mod.volume == 56
    assert mod.pitch == -231
    assert mod.pitch_scale == 18
    assert mod.feedback == 23
    assert mod.grain_size == 35
    assert mod.mode == mod.Mode.lq
