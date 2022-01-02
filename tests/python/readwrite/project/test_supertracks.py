from rv.pattern import Pattern, PatternFlagsPFLG


def test_empty_project(read_write_read_project):
    project = read_write_read_project("supertracks")
    assert project.flags == 1
    pattern1, pattern2, *_ = project.patterns
    assert isinstance(pattern1, Pattern)
    assert isinstance(pattern2, Pattern)
    assert pattern1.flags_PFLG == 0
    assert pattern2.flags_PFLG == PatternFlagsPFLG.continue_notes_at_end
