from rv.api import m


def test_issue54(read_write_read_project):
    project = read_write_read_project("issue54/test1")
    mod0, mod1, mod2, mod3 = project.modules[:4]
    assert mod0 is project.output
    assert isinstance(mod1, m.Reverb)
    assert mod2 is None
    assert isinstance(mod3, m.Reverb)
