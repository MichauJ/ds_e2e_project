# tests/conftest.py
import logging
import pytest

@pytest.fixture(autouse=True)
def reset_logging():
    """Runs before every test — prevents handler duplication."""
    root = logging.getLogger()
    root.handlers.clear()
    yield                      # test runs here
    root.handlers.clear()      # cleanup after test