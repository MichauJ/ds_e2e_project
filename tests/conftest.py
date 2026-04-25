# tests/conftest.py
import logging
import pytest
from ds_e2e_project import setup_logging

@pytest.fixture(autouse=True)
def reset_logging():
    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(logging.NOTSET)
    setup_logging()              # ← re-run setup fresh for each test
    yield
    root.handlers.clear()