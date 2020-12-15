from rv.api import m


def test_feedback(read_write_read_synth):
    mod: m.Feedback = read_write_read_synth("feedback").module
    assert mod.flags == 6291537
    assert mod.name == "Feedback"
    assert mod.volume == 1708
    assert mod.channels == mod.Channels.mono
