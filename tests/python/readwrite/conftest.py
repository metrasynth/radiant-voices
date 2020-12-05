from io import BytesIO
from pathlib import Path

import pytest
from rv.api import Synth, read_sunvox_file


@pytest.fixture
def test_files_path() -> Path:
    return Path(__file__).parent / "../../files"


@pytest.fixture
def read_write_read_sunsynth(test_files_path):
    def _read_write_read_sunsynth(name: str) -> Synth:
        synth = read_sunvox_file(test_files_path / f"{name}.sunsynth")
        f = BytesIO()
        synth.write_to(f)
        f.seek(0)
        synth = read_sunvox_file(f).module
        return synth

    return _read_write_read_sunsynth
