from rv.api import m


def test_issue41(read_write_read_project):
    project = read_write_read_project("issue41/sample")
    delay: m.Delay = project.modules[1]
    assert delay.delay_l == 8192
    assert delay.delay_r == 8192
    assert delay.delay_unit == delay.DelayUnit.hz
