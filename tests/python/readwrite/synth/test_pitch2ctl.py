from rv.api import m


def test_pitch2ctl(read_write_read_synth):
    mod: m.Pitch2Ctl = read_write_read_synth("pitch2ctl").module
    assert mod.flags == 16908361
    assert mod.name == "Pitch2Ctl"
    assert mod.mode == mod.Mode.pitch
    assert mod.note_off_action == mod.NoteOffAction.pitch_down
    assert mod.first_note == 19
    assert mod.range == 217
    assert mod.out_min == 27327
    assert mod.out_max == 7746
    assert mod.out_controller == 239
