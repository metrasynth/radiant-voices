from rv.api import m


def test_multisynth_default_options():
    mod = m.MultiSynth()
    assert mod.use_static_note_C5 is False
    assert mod.ignore_notes_with_zero_velocity is False
    assert mod.active_curve == mod.ActiveCurve.note_velocity
    assert mod.trigger is False
    assert mod.generate_missed_note_off_commands is False
    assert mod.round_note_x is False
    assert mod.round_pitch_y is False
    assert mod.record_notes_to_scale_curve is False
    assert mod.out_note_out_note_minus_in_note_plus_C5 is False
    assert mod.out_port_mode == mod.OutPortMode.all_or_random1
    assert mod.out_port_mode_random is False
