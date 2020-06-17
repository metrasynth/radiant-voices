import pytest
from rv.api import Project, m
from rv.modules.multictl import convert_value

CASES = [
    (256, 2, 0, 32768, 0, 256, 0, 0),
    # gain  qsteps  smin    smax    dmin    dmax    value   expected
    (0, 32768, 0, 32768, 0, 256, 0, 0),
    (0, 32768, 0, 32768, 0, 256, 8192, 0),
    (0, 32768, 0, 32768, 0, 256, 16384, 0),
    (0, 32768, 0, 32768, 0, 256, 24576, 0),
    (0, 32768, 0, 32768, 0, 256, 32768, 0),
    (128, 32768, 0, 32768, 0, 256, 0, 0),
    (128, 32768, 0, 32768, 0, 256, 8192, 32),
    (128, 32768, 0, 32768, 0, 256, 16384, 64),
    (128, 32768, 0, 32768, 0, 256, 24576, 96),
    (128, 32768, 0, 32768, 0, 256, 32768, 128),
    (256, 32768, 0, 32768, 0, 256, 0, 0),
    (256, 32768, 0, 32768, 0, 256, 8192, 64),
    (256, 32768, 0, 32768, 0, 256, 16384, 128),
    (256, 32768, 0, 32768, 0, 256, 24576, 192),
    (256, 32768, 0, 32768, 0, 256, 32768, 256),
    (384, 32768, 0, 32768, 0, 256, 0, 0),
    (384, 32768, 0, 32768, 0, 256, 8192, 96),
    (384, 32768, 0, 32768, 0, 256, 16384, 192),
    (384, 32768, 0, 32768, 0, 256, 24576, 256),
    (384, 32768, 0, 32768, 0, 256, 32768, 256),
    (1024, 32768, 0, 32768, 0, 256, 0, 0),
    (1024, 32768, 0, 32768, 0, 256, 4096, 128),
    (1024, 32768, 0, 32768, 0, 256, 8192, 256),
    (1024, 32768, 0, 32768, 0, 256, 16384, 256),
    (1024, 32768, 0, 32768, 0, 256, 32768, 256),
    (256, 32768, 5000, 25000, 0, 256, 0, 39),
    (256, 32768, 5000, 25000, 0, 256, 8192, 78),
    (256, 32768, 5000, 25000, 0, 256, 16384, 117),
    (256, 32768, 5000, 25000, 0, 256, 24576, 156),
    (256, 32768, 5000, 25000, 0, 256, 32768, 195),
    (256, 32768, 25000, 5000, 0, 256, 0, 195),
    (256, 32768, 25000, 5000, 0, 256, 8192, 156),
    (256, 32768, 25000, 5000, 0, 256, 16384, 117),
    (256, 32768, 25000, 5000, 0, 256, 24576, 78),
    (256, 32768, 25000, 5000, 0, 256, 32768, 39),
    (256, 32768, 32768, 0, 0, 256, 0, 256),
    (256, 32768, 32768, 0, 0, 256, 8192, 192),
    (256, 32768, 32768, 0, 0, 256, 16384, 128),
    (256, 32768, 32768, 0, 0, 256, 24576, 64),
    (256, 32768, 32768, 0, 0, 256, 32768, 0),
    (128, 32768, 32768, 0, 0, 256, 0, 256),
    (128, 32768, 32768, 0, 0, 256, 8192, 224),
    (128, 32768, 32768, 0, 0, 256, 16384, 192),
    (128, 32768, 32768, 0, 0, 256, 24576, 160),
    (128, 32768, 32768, 0, 0, 256, 32768, 128),
    (1024, 32768, 32768, 0, 0, 256, 0, 256),
    (1024, 32768, 32768, 0, 0, 256, 4096, 128),
    (1024, 32768, 32768, 0, 0, 256, 8192, 0),
    (1024, 32768, 32768, 0, 0, 256, 16384, 0),
    (1024, 32768, 32768, 0, 0, 256, 32768, 0),
    (256, 2, 0, 32768, 0, 256, 0, 0),
    (256, 2, 0, 32768, 0, 256, 8192, 0),
    (256, 2, 0, 32768, 0, 256, 16384, 0),
    (256, 2, 0, 32768, 0, 256, 24576, 0),
    (256, 2, 0, 32768, 0, 256, 32768, 256),
    (256, 2, 32768, 0, 0, 256, 0, 256),
    (256, 2, 32768, 0, 0, 256, 8192, 256),
    (256, 2, 32768, 0, 0, 256, 16384, 256),
    (256, 2, 32768, 0, 0, 256, 24576, 256),
    (256, 2, 32768, 0, 0, 256, 32768, 0),
    (256, 3, 0, 32768, 0, 256, 0, 0),
    (256, 3, 0, 32768, 0, 256, 8192, 0),
    (256, 3, 0, 32768, 0, 256, 16384, 128),
    (256, 3, 0, 32768, 0, 256, 24576, 128),
    (256, 3, 0, 32768, 0, 256, 32768, 256),
    (256, 3, 32768, 0, 0, 256, 0, 256),
    (256, 3, 32768, 0, 0, 256, 8192, 256),
    (256, 3, 32768, 0, 0, 256, 16384, 128),
    (256, 3, 32768, 0, 0, 256, 24576, 128),
    (256, 3, 32768, 0, 0, 256, 32768, 0),
    (256, 7, 0, 32768, 0, 256, 0, 0),
    (256, 7, 0, 32768, 0, 256, 8192, 42),
    (256, 7, 0, 32768, 0, 256, 16384, 128),
    (256, 7, 0, 32768, 0, 256, 24576, 170),
    (256, 7, 0, 32768, 0, 256, 32768, 256),
    (256, 7, 32768, 0, 0, 256, 0, 256),
    (256, 7, 32768, 0, 0, 256, 8192, 213),
    (256, 7, 32768, 0, 0, 256, 16384, 128),
    (256, 7, 32768, 0, 0, 256, 24576, 85),
    (256, 7, 32768, 0, 0, 256, 32768, 0),
    (256, 20, 0, 32768, 0, 256, 0, 0),
    (256, 20, 0, 32768, 0, 256, 8192, 53),
    (256, 20, 0, 32768, 0, 256, 16384, 121),
    (256, 20, 0, 32768, 0, 256, 24576, 188),
    (256, 20, 0, 32768, 0, 256, 32768, 256),
    (256, 20, 32768, 0, 0, 256, 0, 256),
    (256, 20, 32768, 0, 0, 256, 8192, 202),
    (256, 20, 32768, 0, 0, 256, 16384, 134),
    (256, 20, 32768, 0, 0, 256, 24576, 67),
    (256, 20, 32768, 0, 0, 256, 32768, 0),
    (256, 61, 0, 32768, 0, 256, 0, 0),
    (256, 61, 0, 32768, 0, 256, 8192, 64),
    (256, 61, 0, 32768, 0, 256, 16384, 128),
    (256, 61, 0, 32768, 0, 256, 24576, 192),
    (256, 61, 0, 32768, 0, 256, 32768, 256),
]


@pytest.mark.parametrize("gain,qsteps,smin,smax,dmin,dmax,value,expected", CASES)
def test_convert_value(gain, qsteps, smin, smax, dmin, dmax, value, expected):
    out = convert_value(
        gain=gain,
        qsteps=qsteps,
        smin=smin,
        smax=smax,
        dmin=dmin,
        dmax=dmax,
        vmax=dmax - dmin if dmax > dmin else dmin - dmax,
        value=value,
    )
    assert out == expected


def test_propagation_amp_volume():
    p = Project()
    amp1 = p.new_module(m.Amplifier)
    amp2 = p.new_module(m.Amplifier)
    mc = p.new_module(m.MultiCtl)
    mc >> amp1
    mc >> amp2
    mc.mappings.values[0].min = 32768
    mc.mappings.values[0].max = 0
    mc.mappings.values[0].controller = amp1.controllers["volume"].number
    mc.mappings.values[1].controller = amp2.controllers["volume"].number
    mc.value = 0
    assert amp1.volume == 1024
    assert amp2.volume == 0
    mc.value = 16384
    assert amp1.volume == 512
    assert amp2.volume == 512
    mc.value = 32768
    assert amp1.volume == 0
    assert amp2.volume == 1024


def test_propagation_multisynth_transpose():
    p = Project()
    ms1 = p.new_module(m.MultiSynth)
    ms2 = p.new_module(m.MultiSynth)
    mc = p.new_module(m.MultiCtl)
    mc >> ms1
    mc >> ms2
    mc.mappings.values[0].min = 0
    mc.mappings.values[0].max = 256
    mc.mappings.values[0].controller = ms1.controllers["transpose"].number
    mc.mappings.values[1].min = 256
    mc.mappings.values[1].max = 0
    mc.mappings.values[1].controller = ms2.controllers["transpose"].number
    mc.value = 0
    assert ms1.transpose == -128
    assert ms2.transpose == 128
    mc.value = 16384
    assert ms1.transpose == 0
    assert ms2.transpose == 0
    mc.value = 32768
    assert ms1.transpose == 128
    assert ms2.transpose == -128


def test_propagation_multisynth_transpose_rangelimit():
    p = Project()
    ms1 = p.new_module(m.MultiSynth)
    mc = p.new_module(m.MultiCtl)
    mc >> ms1
    mapping = mc.mappings.values[0]
    mapping.controller = ms1.controllers["transpose"].number
    mapping.min = 128
    mapping.max = 144
    mapping.gain = 256 + int(256 / 17)
    mc.value = 0
    assert ms1.transpose == 0
    mc.value = 16384
    assert ms1.transpose == 8
    mc.value = 32768
    assert ms1.transpose == 16


def test_reflect():
    p = Project()
    amp1 = p.new_module(m.Amplifier)
    amp2 = p.new_module(m.Amplifier)
    mc = p.new_module(m.MultiCtl)
    mc >> amp1
    mc >> amp2
    mc.mappings.values[0].min = 32768
    mc.mappings.values[0].max = 0
    mc.mappings.values[0].controller = amp1.controllers["volume"].number
    mc.mappings.values[1].controller = amp2.controllers["volume"].number
    amp1.volume = 0
    mc.reflect(0)
    assert mc.value == 32768
    assert amp2.volume == 1024
