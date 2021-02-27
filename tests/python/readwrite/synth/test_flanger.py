from rv.api import m


def test_flanger(read_write_read_synth):
    mod: m.Flanger = read_write_read_synth("flanger").module
    assert mod.flags == 1105
    assert mod.name == "Flanger"
    assert mod.dry == 136
    assert mod.wet == 150
    assert mod.feedback == 22
    assert mod.delay == 93
    assert mod.response == 134
    assert mod.lfo_freq == 102
    assert mod.lfo_amp == 203
    assert mod.lfo_waveform == mod.LfoWaveform.hsin
    assert mod.set_lfo_phase == 37
    assert mod.lfo_freq_unit == mod.LfoFreqUnit.hz_0_05
