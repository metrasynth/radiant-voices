import rv.api


def test_connection_shorthand():
    p = rv.Project()
    amp = p.new_module(rv.modules.Amplifier)
    gen = p.new_module(rv.modules.Generator)
    gen >> amp
    p.output << amp
    assert gen.index in p.module_connections[amp.index]
    assert amp.index in p.module_connections[p.output.index]
