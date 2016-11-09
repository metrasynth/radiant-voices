from rv.api import Project, m


def test_connection_shorthand():
    p = Project()
    amp = p.new_module(m.Amplifier)
    gen = p.new_module(m.Generator)
    gen >> amp
    p.output << amp
    assert gen.index in p.module_connections[amp.index]
    assert amp.index in p.module_connections[p.output.index]
