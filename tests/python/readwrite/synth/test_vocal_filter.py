from rv.api import m


def test_vocal_filter(read_write_read_synth):
    mod: m.VocalFilter = read_write_read_synth("vocal-filter").module
    assert mod.flags == 81
    assert mod.name == "Vocal filter"
    assert mod.volume == 271
    assert mod.formant_width_hz == 249
    assert mod.intensity == 207
    assert mod.formants == 3
    assert mod.vowel == 243
    assert mod.voice_type == mod.VoiceType.bass
    assert mod.channels == mod.Channels.stereo
