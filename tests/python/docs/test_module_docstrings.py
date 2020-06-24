from rv.modules import Generator, Output


def test_output_module_docstring():
    lines = Output.__doc__.splitlines()
    assert lines[0] == '"Output" SunVox Output Module'


def test_generator_module_docstring():
    lines = Generator.__doc__.splitlines()
    assert lines[0] == '"Generator" SunVox Synth Module'
