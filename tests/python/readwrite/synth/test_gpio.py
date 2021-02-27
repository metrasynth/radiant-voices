from rv.api import m


def test_gpio(read_write_read_synth):
    mod: m.Gpio = read_write_read_synth("gpio").module
    assert mod.flags == 81
    assert mod.name == "GPIO"
    assert not mod.out
    assert mod.out_pin == 213
    assert mod.out_threshold == 46
    assert mod.in_
    assert mod.in_pin == 210
    assert mod.in_note == 0
    assert mod.in_amplitude == 93
