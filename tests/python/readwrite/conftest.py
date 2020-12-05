from io import BytesIO
from pathlib import Path

import pytest
from rv.api import Project, Synth, read_sunvox_file


@pytest.fixture
def test_files_path() -> Path:
    return Path(__file__).parent / "../../files"


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
    def _read_write_read_project(name: str) -> Project:
        project = read_sunvox_file(test_files_path / f"{name}.sunvox")
        f = BytesIO()
        project.write_to(f)
        f.seek(0)
        project = read_sunvox_file(f)
        return project

    return _read_write_read_project
