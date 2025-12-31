"""If `sunvox/` is adjacent to this repo, load and save (to memory) all SunVox files

Run with: pytest -m stress
Exclude with: pytest -m "not stress"
"""

from io import BytesIO
from pathlib import Path

import pytest
from rv.api import read_sunvox_file

pytestmark = pytest.mark.stress

sunvox_dir = Path(__file__).parents[4] / "sunvox"
filenames = []
if sunvox_dir.is_dir():
    sunvox_dir = sunvox_dir.absolute().resolve()
    path: Path
    for path in sunvox_dir.glob("**/*.sunvox"):
        filenames.append(path.relative_to(sunvox_dir))
    for path in sunvox_dir.glob("**/*.sunsynth"):
        filenames.append(path.relative_to(sunvox_dir))


def make_test_id(filename):
    return str(filename)


@pytest.mark.parametrize("filename", filenames, ids=make_test_id)
def test_stress(filename):
    path = sunvox_dir / filename
    with path.open("rb") as f:
        obj = read_sunvox_file(f)
    f = BytesIO()
    obj.write_to(f)
    f.seek(0)
    read_sunvox_file(f)
