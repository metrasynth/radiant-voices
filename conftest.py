# Root conftest.py - registers pytest markers

def pytest_configure(config):
    config.addinivalue_line("markers", "stress: stress tests (load all files from sunvox/ directory)")
