from rv.api import m


def test_fft(read_write_read_synth):
    mod: m.Fft = read_write_read_synth("fft").module
    assert mod.flags == 0x02000051
    assert mod.name == "FFT"
    assert mod.sample_rate == mod.SampleRate._44100hz
    assert mod.channels == mod.Channels.mono
    assert mod.buffer == mod.Buffer._128
    assert mod.buf_overlap == mod.BufferOverlap._4x
    assert mod.feedback == 5064
    assert mod.noise_reduction == 27057
    assert mod.phase_gain == 9600
    assert mod.all_pass_filter == 12317
    assert mod.frequency_spread == 13403
    assert mod.random_phase == 18439
    assert mod.random_phase_lite == 9270
    assert mod.freq_shift == 3913
    assert mod.deform1 == 3948
    assert mod.deform2 == 19358
    assert mod.hp_cutoff == 25357
    assert mod.lp_cutoff == 12632
    assert mod.volume == 13740
