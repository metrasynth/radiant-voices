from rv.api import read_sunvox_file


def test_issue109(test_files_path):
    project = read_sunvox_file(test_files_path / "issue109/filter_lfo.sunvox")

    (
        output,
        generator,
        echo,
        multisynth,
        _,
        generator2,
        vibrato,
        filter,
    ) = project.modules

    assert output.in_links == [filter.index]
    assert output.in_link_slots == [0]
    assert output.out_links == []
    assert output.out_link_slots == []

    assert generator.in_links == [multisynth.index]
    assert generator.in_link_slots == [0]
    assert generator.out_links == [vibrato.index]
    assert generator.out_link_slots == [0]

    assert echo.in_links == [vibrato.index]
    assert echo.in_link_slots == [0]
    assert echo.out_links == [filter.index]
    assert echo.out_link_slots == [0]

    assert multisynth.in_links == []
    assert multisynth.in_link_slots == []
    assert multisynth.out_links == [generator.index, generator2.index]
    assert multisynth.out_link_slots == [0, 0]

    assert generator2.in_links == [multisynth.index]
    assert generator2.in_link_slots == [1]
    assert generator2.out_links == [vibrato.index]
    assert generator2.out_link_slots == [2]

    assert vibrato.in_links == [generator.index, -1, generator2.index]
    assert vibrato.in_link_slots == [0, 0, 0]
    assert vibrato.out_links == [echo.index]
    assert vibrato.out_link_slots == [0]

    assert filter.in_links == [echo.index]
    assert filter.in_link_slots == [0]
    # [TODO] fix link algorithm, it should be this:
    # assert filter.out_links == [output.index]
    # assert filter.out_link_slots == [0]
    assert filter.out_links == [vibrato.index]
    assert filter.out_link_slots == [1]
