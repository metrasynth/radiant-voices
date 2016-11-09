from rv.api import Project, m


def test_layout():
    p = Project()
    out = p.output
    gen1 = p.new_module(m.Generator)
    gen2 = p.new_module(m.Generator)
    amp = p.new_module(m.Amplifier)
    amp << [gen1, gen2]
    amp >> out
    assert [gen1.x, gen2.x, amp.x, out.x].count(512) == 4
    assert [gen1.y, gen2.y, amp.y, out.y].count(512) == 4
    p.layout()
    assert [gen1.x, gen2.x, amp.x, out.x].count(512) != 4
    assert [gen1.y, gen2.y, amp.y, out.y].count(512) != 4
