from struct import pack

from pytest import raises
from rv.api import m
from rv.lib.conversions import base2_to_base10


def test_single_fm(read_write_read_project):
    project = read_write_read_project("single-fm")
    assert project.name == "single fm"

    assert project.receive_sync_midi == project.SyncCommand.tempo
    assert (
        project.receive_sync_other
        == project.SyncCommand.start_stop | project.SyncCommand.position
    )

    assert project.initial_bpm == 126
    assert project.initial_tpl == 7
    assert project.global_volume == 80
    assert project.sunvox_version == (1, 9, 5, 2)
    assert project.based_on_version == (1, 9, 5, 2)
    assert len(project.modules) == 2
    output = project.output
    assert output.finetune == 0
    assert output.relative_note == 0
    assert output.layer == 0
    assert base2_to_base10(output.scale) == 100
    fm = project.modules[1]
    assert isinstance(fm, m.Fm)
    assert fm.name == "FM"
    assert fm.c_volume == 129
    assert fm.m_volume == 49
    assert fm.panning == 1
    assert fm.c_freq_ratio == 2
    assert fm.m_freq_ratio == 2
    assert fm.m_feedback == 1
    assert fm.c_attack == 33
    assert fm.c_decay == 33
    assert fm.c_sustain == 129
    assert fm.c_release == 65
    assert fm.c_attack == 33
    assert fm.m_decay == 33
    assert fm.m_sustain == 129
    assert fm.m_release == 65
    assert fm.m_scaling_per_key == 1
    assert fm.polyphony_ch == 5
    assert fm.mode == fm.Mode.lq


def test_single_fm_writes_correct_chunks(read_write_read_project):
    project = read_write_read_project("single-fm")
    chunks = project.chunks()

    def v():
        return next(chunks)

    def expect_chunk(*chunk):
        assert v() == chunk

    def expect_cval(value):
        expect_chunk(b"CVAL", pack("<i", value))

    expect_chunk(b"SVOX", b"")
    expect_chunk(b"VERS", b"\x02\x05\x09\x01")
    expect_chunk(b"BVER", b"\x02\x05\x09\x01")
    expect_chunk(b"SFGS", b"\x2a\0\0\0")
    expect_chunk(b"BPM ", b"\x7e\0\0\0")
    expect_chunk(b"SPED", b"\7\0\0\0")
    expect_chunk(b"TGRD", b"\3\0\0\0")
    expect_chunk(b"TGD2", b"\5\0\0\0")
    expect_chunk(b"GVOL", b"\x50\0\0\0")
    expect_chunk(b"NAME", b"single fm\0")
    expect_chunk(b"MSCL", b"\0\1\0\0")
    expect_chunk(b"MZOO", b"\x60\1\0\0")
    expect_chunk(b"MXOF", b"\0\0\0\0")
    expect_chunk(b"MYOF", b"\0\0\0\0")
    expect_chunk(b"LMSK", b"\0\0\0\0")
    expect_chunk(b"CURL", b"\0\0\0\0")
    expect_chunk(b"TIME", b"\xd3\xff\xff\xff")
    expect_chunk(b"SELS", b"\1\0\0\0")
    expect_chunk(b"LGEN", b"\1\0\0\0")
    expect_chunk(b"PATN", b"\0\0\0\0")
    expect_chunk(b"PATT", b"\1\0\0\0")
    expect_chunk(b"PATL", b"\1\0\0\0")
    expect_chunk(
        b"PDTA",
        b"\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00"
        b"10\x02\x00\x00\x03gE"
        b"\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00",
    )
    expect_chunk(b"PCHN", b"\2\0\0\0")
    expect_chunk(b"PLIN", b"\4\0\0\0")
    expect_chunk(b"PYSZ", b"\x20\0\0\0")
    expect_chunk(b"PFLG", b"\0\0\0\0")
    expect_chunk(
        b"PICO",
        b"\xd4+\x1ex\xc5\xa3\xed\xb7"
        b"\xe4'\x15\xa8\xd8\x1b\x11\x88"
        b"\x9d\xb9\xf7\xef\x13\xc8\xc6c"
        b"\xbe}\xcd\xb3|>\xbb\xdd",
    )
    expect_chunk(b"PFGC", b"\0\0\0")
    expect_chunk(b"PBGC", b"\xff\xff\xff")
    expect_chunk(b"PFFF", b"\0\0\0\0")
    expect_chunk(b"PXXX", b"\0\0\0\0")
    expect_chunk(b"PYYY", b"\0\0\0\0")
    expect_chunk(b"PEND", b"")
    expect_chunk(b"PPAR", b"\0\0\0\0")
    expect_chunk(b"PFFF", b"\3\0\0\0")
    expect_chunk(b"PXXX", b"\4\0\0\0")
    expect_chunk(b"PYYY", b"\0\0\0\0")
    expect_chunk(b"PEND", b"")

    expect_chunk(b"SFFF", b"\x43\0\0\0")
    expect_chunk(b"SNAM", b"Output" + b"\0" * (32 - 6))
    expect_chunk(b"SFIN", b"\0\0\0\0")
    expect_chunk(b"SREL", b"\0\0\0\0")
    expect_chunk(b"SXXX", b"\0\2\0\0")
    expect_chunk(b"SYYY", b"\0\2\0\0")
    expect_chunk(b"SZZZ", b"\0\0\0\0")
    expect_chunk(b"SSCL", b"\0\1\0\0")
    expect_chunk(b"SVPR", b"\xc2\x02\x32\x9a")
    expect_chunk(b"SCOL", b"\xff\xff\xff")
    expect_chunk(b"SMII", b"\0\0\0\0")
    expect_chunk(b"SMIC", b"\0\0\0\0")
    expect_chunk(b"SMIB", b"\xff\xff\xff\xff")
    expect_chunk(b"SMIP", b"\xff\xff\xff\xff")
    expect_chunk(b"SLNK", b"\1\0\0\0")
    expect_chunk(b"SLnK", b"\0\0\0\0")
    expect_chunk(b"SEND", b"")
    expect_chunk(b"SFFF", b"\x49\0\0\0")
    expect_chunk(b"SNAM", b"FM" + b"\0" * (32 - 2))
    expect_chunk(b"STYP", b"FM\0")
    expect_chunk(b"SFIN", b"\1\0\0\0")
    expect_chunk(b"SREL", b"\1\0\0\0")
    expect_chunk(b"SXXX", b"\x38\1\0\0")
    expect_chunk(b"SYYY", b"\x08\2\0\0")
    expect_chunk(b"SZZZ", b"\0\0\0\0")
    expect_chunk(b"SSCL", b"\0\1\0\0")
    expect_chunk(b"SVPR", b"\xc2\x02\x32\x9a")
    expect_chunk(b"SCOL", b"\0\xe3\xff")
    expect_chunk(b"SMII", b"\0\0\0\0")
    expect_chunk(b"SMIC", b"\0\0\0\0")
    expect_chunk(b"SMIB", b"\xff\xff\xff\xff")
    expect_chunk(b"SMIP", b"\xff\xff\xff\xff")
    expect_chunk(b"SLNK", b"")
    expect_chunk(b"SLnK", b"")

    expect_cval(0x81)
    expect_cval(0x31)
    expect_cval(0x81)
    expect_cval(2)
    expect_cval(2)
    expect_cval(1)
    expect_cval(0x21)
    expect_cval(0x21)
    expect_cval(0x81)
    expect_cval(0x41)
    expect_cval(0x21)
    expect_cval(0x21)
    expect_cval(0x81)
    expect_cval(0x41)
    expect_cval(1)
    expect_cval(5)
    expect_cval(2)

    expect_chunk(
        b"CMID",
        b"\x00\x00\x00\x00\x00\x00\x00\xff"
        b"\x00\x00\x00\x00\x00\x00\x00\xff"
        b"\x00\x00\x00\x00\x00\x00\x00\xff"
        b"\x00\x00\x00\x00\x00\x00\x00\xff"
        b"\x00\x00\x00\x00\x00\x00\x00\xff"
        b"\x00\x00\x00\x00\x00\x00\x00\xff"
        b"\x00\x00\x00\x00\x00\x00\x00\xff"
        b"\x00\x00\x00\x00\x00\x00\x00\xff"
        b"\x00\x00\x00\x00\x00\x00\x00\xff"
        b"\x00\x00\x00\x00\x00\x00\x00\xff"
        b"\x00\x00\x00\x00\x00\x00\x00\xff"
        b"\x00\x00\x00\x00\x00\x00\x00\xff"
        b"\x00\x00\x00\x00\x00\x00\x00\xff"
        b"\x00\x00\x00\x00\x00\x00\x00\xff"
        b"\x00\x00\x00\x00\x00\x00\x00\xff"
        b"\x00\x00\x00\x00\x00\x00\x00\xff"
        b"\x00\x00\x00\x00\x00\x00\x00\xff",
    )
    expect_chunk(b"SEND", b"")
    with raises(StopIteration):
        expect_chunk(b"", b"")
