from rv.api import m


def test_vocal_filter(read_write_read_synth):
    mod: m.VocalFilter = read_write_read_synth("vocal-filter").module
    assert mod.flags == 0x02000051
    assert mod.name == "Vocal filter"
    assert mod.volume == 271
    assert mod.formant_width == 249
    assert mod.intensity == 207
    assert mod.formants == 3
    assert mod.vowel == 243
    assert mod.voice_type == mod.VoiceType.bass
    assert mod.channels == mod.Channels.stereo
    assert mod.random_frequency == 726
    assert mod.random_seed == 10401
    assert mod.vowel1 == mod.Vowel.o
    assert mod.vowel2 == mod.Vowel.u
    assert mod.vowel3 == mod.Vowel.o
    assert mod.vowel4 == mod.Vowel.i
    assert mod.vowel5 == mod.Vowel.e
