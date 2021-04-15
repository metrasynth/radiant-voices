from pathlib import Path

import pytest
from rv.api import read_sunvox_file

# (Cannot get at the fixture version of this within pytest_generate_tests)
CUR_PATH = Path(__file__).parent
EXTRA_FILES_PATH = CUR_PATH / "../../files/extra"
EXTRA_FILES = [str(x) for x in EXTRA_FILES_PATH.rglob("*.sunvox")]
EXTRA_FILES += [str(x) for x in EXTRA_FILES_PATH.rglob("*.sunsynth")]
EXTRA_FILES.sort()


@pytest.mark.parametrize("path", EXTRA_FILES)
def test_extra_files(path):
    read_sunvox_file(path)
