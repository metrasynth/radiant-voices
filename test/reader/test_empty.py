from rv.reader import read_sunvox_file
from rv.structure.conversions import base2_to_base10

from .base import FIXTURE_DIR


def test_empty():
    f = read_sunvox_file(str(FIXTURE_DIR / 'empty.sunvox'))
    assert f.project.name == 'empty'
    assert f.project.initial_bpm == 125
    assert f.project.initial_tpl == 6
    assert base2_to_base10(f.project.global_volume) == 100
    assert f.project.sunvox_version == (1, 9, 1, 0)
    assert f.project.based_on_version == (1, 2, 3, 4)
    assert len(f.modules) == 1
    output = f.modules[0]
    assert output.name == 'Output'
    assert output.finetune == 0
    assert output.relative_note == 0
    assert output.z == 0
    assert base2_to_base10(output.scale) == 100
    assert output.visualization.background == Opacity.NORMAL
    assert output.visualization.shadow == Opacity.OFF
    assert output.visualization.level_meter == LevelMeter.MONO
    assert output.visualization.level_orientation == LevelOrientation.HORIZONTAL
    assert output.visualization.oscilloscope == Oscilloscope.POINTS
    assert output.visualization.oscilloscope_buffer_size_ms == 12
