import pytest
from rv.api import Project, m


@pytest.fixture
def project():
    return Project()


def test_initial_project(project):
    assert isinstance(project.output, m.Output)
    assert len(project.modules) == 1
    assert project.modules[0] is project.output
    assert len(project.patterns) == 0
    assert project.sunvox_version == (1, 9, 6, 1)
    assert project.based_on_version == (1, 9, 6, 1)
    assert project.initial_bpm == 125
    assert project.initial_tpl == 6
    assert project.global_volume == 80
    assert project.name == "Project"
    assert project.time_grid == 4
    assert project.modules_scale == 256
    assert project.modules_zoom == 256
    assert project.modules_x_offset == 0
    assert project.modules_y_offset == 0
    assert project.modules_layer_mask == 0x00000000
    assert project.modules_current_layer == 0
    assert project.timeline_position == 0
    assert project.selected_module == 0
    assert project.current_pattern == 0
    assert project.current_track == 0
    assert project.current_line == 1
