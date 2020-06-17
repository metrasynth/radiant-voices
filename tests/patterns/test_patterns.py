import pytest
from rv.api import Pattern, Project, m
from rv.errors import PatternOwnershipError


def test_pattern_starts_with_no_project():
    empty_pattern = Pattern(tracks=1, lines=4)
    assert empty_pattern.project is None


def test_pattern_project_is_set_after_attaching():
    empty_pattern = Pattern(tracks=1, lines=4)
    project = Project()
    project.attach_pattern(empty_pattern)
    assert empty_pattern.project is project


def test_pattern_cannot_be_attached_to_multiple_projects():
    empty_pattern = Pattern(tracks=1, lines=4)
    project = Project()
    project.attach_pattern(empty_pattern)
    project2 = Project()
    with pytest.raises(PatternOwnershipError):
        project2.attach_pattern(empty_pattern)


def test_note_belongs_to_pattern():
    empty_pattern = Pattern(tracks=1, lines=4)
    note = empty_pattern.data[0][0]
    assert note.pattern is empty_pattern


def test_note_belongs_to_project_of_pattern():
    empty_pattern = Pattern(tracks=1, lines=4)
    note = empty_pattern.data[0][0]
    assert note.project is None
    project = Project()
    project.attach_pattern(empty_pattern)
    assert note.project is project


def test_note_mod_property():
    project = Project()
    pattern = Pattern(tracks=1, lines=4)
    project.attach_pattern(pattern)
    note = pattern.data[0][0]
    assert note.module == 0
    assert note.module_index is None
    assert note.mod is None
    mod: m.Generator = project.new_module(m.Generator)
    note.mod = mod
    assert note.mod is mod
    assert note.module_index == mod.index
    assert note.module == mod.index + 1
    note.module = 5
    assert note.mod is None
    assert note.module_index == 4
