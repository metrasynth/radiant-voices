from rv import modules
from rv.lib.conversions import base2_to_base10
from rv.readers.reader import read_sunvox_file

from .base import FIXTURE_DIR


def test_empty():
    project = read_sunvox_file(str(FIXTURE_DIR / "empty.sunvox"))
    assert project.name == "empty"
    assert project.initial_bpm == 125
    assert project.initial_tpl == 6
    assert base2_to_base10(project.global_volume) == 31
    assert project.sunvox_version == (2, 1, 2, 1)
    assert project.based_on_version == (2, 0, 0, 0)
    assert project.flags == 0
    assert len(project.modules) == 1
    output = project.modules[0]
    assert isinstance(output, modules.Output)
    assert output.mod_finetune == 0
    assert output.mod_relative_note == 0
    assert output.layer == 0
    assert base2_to_base10(output.scale) == 100
