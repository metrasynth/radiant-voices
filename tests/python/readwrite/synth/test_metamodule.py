from rv.api import m


def test_metamodule(read_write_read_synth):
    mod: m.MetaModule = read_write_read_synth("metamodule").module
    assert mod.flags == 32841
    assert mod.name == "MetaModule"

    assert [mapping.__dict__ for mapping in mod.mappings.values] == EXPECTED_MAPPINGS
    assert [c.label for c in mod.user_defined] == EXPECTED_CONTROLLER_NAMES

    assert mod.volume == 149
    assert mod.input_module == 1
    assert mod.play_patterns == mod.PlayPatterns.on_no_repeat
    assert mod.bpm == 560
    assert mod.tpl == 30

    assert mod.user_defined_controllers == 2
    assert not mod.arpeggiator
    assert not mod.apply_velocity_to_project
    assert mod.event_output
    assert not mod.receive_notes_from_keyboard
    assert not mod.do_not_receive_notes_from_keyboard

    mod.receive_notes_from_keyboard = True
    assert mod.receive_notes_from_keyboard
    assert not mod.do_not_receive_notes_from_keyboard

    mod.do_not_receive_notes_from_keyboard = True
    assert not mod.receive_notes_from_keyboard
    assert mod.do_not_receive_notes_from_keyboard

    project = mod.project
    assert isinstance(project.modules[0], m.Output)
    assert isinstance(project.modules[1], m.AnalogGenerator)


EXPECTED_MAPPINGS = [
    {"module": 1, "controller": 0},
    {"module": 1, "controller": 1},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
    {"module": 0, "controller": 0},
]


EXPECTED_CONTROLLER_NAMES = [
    "V",
    "W",
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
]
