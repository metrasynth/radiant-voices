from rv.api import m


def test_lfo(read_write_read_synth):
    mod: m.Lfo = read_write_read_synth("lfo").module
    assert mod.flags == 1105
    assert mod.name == "LFO"
    assert mod.volume == 440
    assert mod.type == mod.Type.amplitude
    assert mod.freq == 66
    assert mod.waveform == mod.Waveform.square
    assert mod.set_phase == 77
    assert mod.channels == mod.Channels.stereo
    assert mod.frequency_unit == mod.FrequencyUnit.tick
    assert mod.duty_cycle == 64
    assert not mod.generator
