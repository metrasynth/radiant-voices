from rv.api import m


def test_vorbis_player(read_write_read_synth):
    mod: m.VorbisPlayer = read_write_read_synth("vorbis-player").module
    assert mod.flags == 32841 | 33554432
    assert mod.name == "moo"
    assert len(mod.data) == 10785
    assert not mod.original_speed
    assert mod.finetune == -38
    assert mod.transpose == 16
    assert mod.interpolation
    assert mod.polyphony == 3
    assert mod.ignore_note_off is True
    assert not mod.repeat
