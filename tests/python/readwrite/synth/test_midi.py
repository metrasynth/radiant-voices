from rv.api import m


def test_midi_in_never(read_write_read_synth):
    mod: m.Module = read_write_read_synth("midi-in-never").module
    assert mod.midi_in_always is False
    assert mod.midi_in_never is True
    assert mod.midi_in_channel == 0


def test_midi_in_always(read_write_read_synth):
    mod: m.Module = read_write_read_synth("midi-in-always").module
    assert mod.midi_in_always is True
    assert mod.midi_in_never is False
    assert mod.midi_in_channel == 1


def test_midi_in_when_selected(read_write_read_synth):
    mod: m.Module = read_write_read_synth("midi-in-when-selected").module
    assert mod.midi_in_always is False
    assert mod.midi_in_never is False
    assert mod.midi_in_channel == 2
