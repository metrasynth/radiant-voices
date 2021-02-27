from rv.api import m


def test_filter_pro(read_write_read_synth):
    mod: m.FilterPro = read_write_read_synth("filter-pro").module
    assert mod.flags == 1105
    assert mod.name == "Filter Pro"
    assert mod.volume == 25562
    assert mod.type == mod.Type.lp
    assert mod.freq_hz == 21049
    assert mod.freq_finetune == -944
    assert mod.freq_scale == 63
    assert mod.exponential_freq
    assert mod.q == 7962
    assert mod.gain == 2934
    assert mod.roll_off == mod.RollOff.db_36
    assert mod.response == 956
    assert mod.mode == mod.Mode.mono
    assert mod.mix == 1945
    assert mod.lfo_freq == 452
    assert mod.lfo_amp == 29983
    assert mod.lfo_waveform == mod.LfoWaveform.saw
    assert mod.set_lfo_phase == 30
    assert mod.lfo_freq_unit == mod.LfoFreqUnit.line_3
