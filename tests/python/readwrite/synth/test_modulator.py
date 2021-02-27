from rv.api import m


def test_modulator(read_write_read_synth):
    mod: m.Modulator = read_write_read_synth("modulator").module
    assert mod.flags == 8273
    assert mod.name == "Modulator"
    assert mod.volume == 141
    assert mod.modulation_type == mod.ModulationType.phase_abs
    assert mod.channels == mod.Channels.mono
