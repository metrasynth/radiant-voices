import logging
from contextlib import contextmanager
from io import BytesIO
from pathlib import Path

import pytest
from rv.api import Project, Synth, m, read_sunvox_file
from rv.lib.iff import dump_file

DEFAULT_TEST_LOG_LEVEL = logging.WARNING


def pytest_configure(config):
    logging.basicConfig(level=DEFAULT_TEST_LOG_LEVEL)


@pytest.fixture
def test_files_path() -> Path:
    return Path(__file__).parent / "../files"


@pytest.fixture
def read_write_read_synth(test_files_path):
    def _read_write_read_synth(name: str) -> Synth:
        synth = read_sunvox_file(path := test_files_path / f"{name}.sunsynth")
        f = BytesIO()
        synth.write_to(f)
        f.seek(0)
        synth = read_sunvox_file(f)
        synth.module.path = path  # for inspecting original file as needed
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


@pytest.fixture
def dump_on_failure():
    """
    Context manager to print a hex dump of the module on failure.

    Include the fixture and then use it like this:

        with dump_on_failure(mod):  # or mod.path to dump the original file
            assert mod.custom_waveform.values == EXPECTED_CUSTOM_WAVEFORM
    """

    @contextmanager
    def _dump_on_failure(module: m.Module | Path):
        try:
            yield
        except Exception:
            from rv.lib.iff import dump_file

            if isinstance(module, m.Module):
                f = BytesIO()
                synth = Synth(module)
                synth.write_to(f)
                f.seek(0)
            elif isinstance(module, Path):
                f = module.open("rb")
            else:
                raise TypeError(f"Don't know how to dump {type(module)}")
            dump_file(f)
            raise

    return _dump_on_failure
