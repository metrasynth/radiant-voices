from io import BytesIO
from pathlib import Path

import pytest
from rv.api import Project, Synth, read_sunvox_file
from rv.lib.iff import dump_file


@pytest.fixture
def test_files_path() -> Path:
    return Path(__file__).parent / "../files"


@pytest.fixture
def read_write_read_synth(test_files_path):
    def _read_write_read_synth(name: str) -> Synth:
        synth = read_sunvox_file(test_files_path / f"{name}.sunsynth")
        f = BytesIO()
        synth.write_to(f)
        f.seek(0)
        synth = read_sunvox_file(f)
        return synth

    return _read_write_read_synth


@pytest.fixture
def read_write_read_project(test_files_path):
    def _read_write_read_project(name: str, verbose=False) -> Project:
        project_path = test_files_path / f"{name}.sunvox"
        with project_path.open("rb") as in_f:
            if verbose:
                print(f"Reading {project_path!r}")
            project = read_sunvox_file(project_path)
            if verbose:
                print("Dumping original contents")
                in_f.seek(0)
                dump_file(in_f)
        if verbose:
            print("Writing to new stream")
        f = BytesIO()
        project.write_to(f)
        f.seek(0)
        if verbose:
            print("Dumping written contents")
            dump_file(f)
            f.seek(0)
            print("Reading from stream")
        project = read_sunvox_file(f)
        return project

    return _read_write_read_project
