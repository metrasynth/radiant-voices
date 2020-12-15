from rv.api import m


def test_filter(read_write_read_synth):
    mod: m.Filter = read_write_read_synth("filter").module
    assert mod.flags == 1105
    assert mod.name == "Filter"
    assert mod.volume == 172
    assert mod.freq == 10617
    assert mod.type == mod.Type.notch
    assert mod.response == 91
    assert mod.mode == mod.Mode.lq
    assert mod.impulse == 11576
    assert mod.mix == 106
    assert mod.lfo_freq == 474
    assert mod.lfo_amp == 250
    assert mod.set_lfo_phase == 32
    assert not mod.exponential_freq
    assert mod.roll_off == mod.RollOff.db_36
    assert mod.lfo_freq_unit == mod.LfoFreqUnit.hz
    assert mod.lfo_waveform == mod.LfoWaveform.saw
