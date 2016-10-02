import rv


def test_layout():
    p = rv.Project()
    out = p.output
    gen1 = p.new_module(rv.modules.Generator)
    gen2 = p.new_module(rv.modules.Generator)
    amp = p.new_module(rv.modules.Amplifier)
    amp << [gen1, gen2]
    amp >> out
    assert [gen1.x, gen2.x, amp.x, out.x].count(512) == 4
    assert [gen1.y, gen2.y, amp.y, out.y].count(512) == 4
    p.layout()
    assert [gen1.x, gen2.x, amp.x, out.x].count(512) != 4
    assert [gen1.y, gen2.y, amp.y, out.y].count(512) != 4
