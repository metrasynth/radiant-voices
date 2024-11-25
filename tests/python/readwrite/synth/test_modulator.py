from rv.api import m


def test_modulator(read_write_read_synth):
    mod: m.Modulator = read_write_read_synth("modulator").module
    assert mod.flags == 8273 | 33554432
    assert mod.name == "Modulator"
    assert mod.volume == 141
    assert mod.modulation_type == mod.ModulationType.max_abs
    assert mod.channels == mod.Channels.mono
    assert mod.max_phase_modulation_delay == mod.MaxPhaseModulationDelay.sec_0_5
