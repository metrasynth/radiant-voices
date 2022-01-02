def test_empty_project(read_write_read_project):
    project = read_write_read_project("supertracks")
    assert project.flags == 1
