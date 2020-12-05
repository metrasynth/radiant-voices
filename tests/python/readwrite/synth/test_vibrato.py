from rv.api import m


def test_vibrato(read_write_read_synth):
    mod: m.Vibrato = read_write_read_synth("vibrato").module
    assert mod.flags == 1105
    assert mod.name == "Vibrato"
    assert mod.volume == 122
    assert mod.amplitude == 228
    assert mod.freq == 1403
    assert mod.channels == mod.Channels.stereo
    assert mod.set_phase == 117
    assert mod.frequency_unit == mod.FrequencyUnit.line
    assert mod.exponential_amplitude
