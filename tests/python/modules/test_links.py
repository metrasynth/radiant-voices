from dataclasses import dataclass
from io import BytesIO

import pytest
from rv.api import Project, m, read_sunvox_file


@dataclass
class ProjectObjects:
    project: Project
    mod1: m.Amplifier
    mod2: m.Amplifier
    mod3: m.Amplifier
    mod4: m.Amplifier

    def write_read(self):
        f = BytesIO()
        self.project.write_to(f)
        f.seek(0)
        project = self.project = read_sunvox_file(f)
        self.mod1, self.mod2, self.mod3, self.mod4 = project.modules[1:]


@pytest.fixture
def project_objects() -> ProjectObjects:
    return ProjectObjects(
        project=(project := Project()),
        mod1=project.new_module(m.Amplifier),
        mod2=project.new_module(m.Amplifier),
        mod3=project.new_module(m.Amplifier),
        mod4=project.new_module(m.Amplifier),
    )


def test_linkfrom_module_module(project_objects):
    p = project_objects
    result = p.mod1 << p.mod2 << p.mod3 << p.mod4
    assert result is p.mod4
    p.write_read()
    assert p.mod1.in_links == [p.mod2.index]
    assert p.mod2.in_links == [p.mod3.index]
    assert p.mod3.in_links == [p.mod4.index]
    assert p.mod4.in_links == []
    assert p.mod1.in_link_slots == [0]
    assert p.mod2.in_link_slots == [0]
    assert p.mod3.in_link_slots == [0]
    assert p.mod4.in_link_slots == []
    assert p.mod1.out_links == []
    assert p.mod2.out_links == [p.mod1.index]
    assert p.mod3.out_links == [p.mod2.index]
    assert p.mod4.out_links == [p.mod3.index]
    assert p.mod1.out_link_slots == []
    assert p.mod2.out_link_slots == [0]
    assert p.mod3.out_link_slots == [0]
    assert p.mod4.out_link_slots == [0]


def test_linkto_module_module(project_objects):
    p = project_objects
    result = p.mod1 >> p.mod2 >> p.mod3 >> p.mod4
    assert result is p.mod4
    p.write_read()
    assert p.mod1.in_links == []
    assert p.mod2.in_links == [p.mod1.index]
    assert p.mod3.in_links == [p.mod2.index]
    assert p.mod4.in_links == [p.mod3.index]
    assert p.mod1.in_link_slots == []
    assert p.mod2.in_link_slots == [0]
    assert p.mod3.in_link_slots == [0]
    assert p.mod4.in_link_slots == [0]
    assert p.mod1.out_links == [p.mod2.index]
    assert p.mod2.out_links == [p.mod3.index]
    assert p.mod3.out_links == [p.mod4.index]
    assert p.mod4.out_links == []
    assert p.mod1.out_link_slots == [0]
    assert p.mod2.out_link_slots == [0]
    assert p.mod3.out_link_slots == [0]
    assert p.mod4.out_link_slots == []


def test_linkfrom_module_modules(project_objects):
    p = project_objects
    result = p.mod1 << [p.mod2, p.mod3, p.mod4]
    assert isinstance(result, list)
    p.write_read()
    assert p.mod1.in_links == [p.mod2.index, p.mod3.index, p.mod4.index]
    assert p.mod2.in_links == []
    assert p.mod3.in_links == []
    assert p.mod4.in_links == []
    assert p.mod1.in_link_slots == [0, 0, 0]
    assert p.mod2.in_link_slots == []
    assert p.mod3.in_link_slots == []
    assert p.mod4.in_link_slots == []
    assert p.mod1.out_links == []
    assert p.mod2.out_links == [p.mod1.index]
    assert p.mod3.out_links == [p.mod1.index]
    assert p.mod4.out_links == [p.mod1.index]
    assert p.mod1.out_link_slots == []
    assert p.mod2.out_link_slots == [0]
    assert p.mod3.out_link_slots == [1]
    assert p.mod4.out_link_slots == [2]
    p.mod1 << ~p.mod3
    assert p.mod1.in_links == [p.mod2.index, -1, p.mod4.index]
    assert p.mod1.in_link_slots == [0, -1, 0]
    assert p.mod2.out_link_slots == [0]
    assert p.mod3.out_link_slots == [-1]
    assert p.mod4.out_link_slots == [2]


def test_linkto_module_modules(project_objects):
    p = project_objects
    result = p.mod1 >> [p.mod2, p.mod3, p.mod4]
    assert isinstance(result, list)
    p.write_read()
    assert p.mod1.in_links == []
    assert p.mod2.in_links == [p.mod1.index]
    assert p.mod3.in_links == [p.mod1.index]
    assert p.mod4.in_links == [p.mod1.index]
    assert p.mod1.in_link_slots == []
    assert p.mod2.in_link_slots == [0]
    assert p.mod3.in_link_slots == [1]
    assert p.mod4.in_link_slots == [2]
    assert p.mod1.out_links == [p.mod2.index, p.mod3.index, p.mod4.index]
    assert p.mod2.out_links == []
    assert p.mod3.out_links == []
    assert p.mod4.out_links == []
    assert p.mod1.out_link_slots == [0, 0, 0]
    assert p.mod2.out_link_slots == []
    assert p.mod3.out_link_slots == []
    assert p.mod4.out_link_slots == []


def test_linkfrom_modules_modules(project_objects):
    p = project_objects
    p.mod1 << [p.mod2, p.mod3] << p.mod4
    p.write_read()
    assert p.mod1.in_links == [p.mod2.index, p.mod3.index]
    assert p.mod2.in_links == [p.mod4.index]
    assert p.mod3.in_links == [p.mod4.index]
    assert p.mod4.in_links == []
    assert p.mod1.in_link_slots == [0, 0]
    assert p.mod2.in_link_slots == [0]
    assert p.mod3.in_link_slots == [1]
    assert p.mod4.in_link_slots == []
    assert p.mod1.out_links == []
    assert p.mod2.out_links == [p.mod1.index]
    assert p.mod3.out_links == [p.mod1.index]
    assert p.mod4.out_links == [p.mod2.index, p.mod3.index]
    assert p.mod1.out_link_slots == []
    assert p.mod2.out_link_slots == [0]
    assert p.mod3.out_link_slots == [1]
    assert p.mod4.out_link_slots == [0, 0]


def test_linkfrom_and_linkto(project_objects):
    p = project_objects
    p.mod1 << [p.mod2, p.mod3] >> p.mod4
    p.write_read()
    assert p.mod1.in_links == [p.mod2.index, p.mod3.index]
    assert p.mod2.in_links == []
    assert p.mod3.in_links == []
    assert p.mod4.in_links == [p.mod2.index, p.mod3.index]
    assert p.mod1.in_link_slots == [0, 0]
    assert p.mod2.in_link_slots == []
    assert p.mod3.in_link_slots == []
    assert p.mod4.in_link_slots == [1, 1]
    assert p.mod1.out_links == []
    assert p.mod2.out_links == [p.mod1.index, p.mod4.index]
    assert p.mod3.out_links == [p.mod1.index, p.mod4.index]
    assert p.mod4.out_links == []
    assert p.mod1.out_link_slots == []
    assert p.mod2.out_link_slots == [0, 0]
    assert p.mod3.out_link_slots == [1, 1]
    assert p.mod4.out_link_slots == []
