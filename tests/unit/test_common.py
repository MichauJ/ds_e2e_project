# tests/unit/test_common.py

import pytest
from pathlib import Path
from box import ConfigBox
from ensure import EnsureError
from ds_e2e_project.utils.common import read_yaml


# ── fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture
def valid_yaml_file(tmp_path):
    """Creates a real temporary YAML file with content."""
    file = tmp_path / "config.yaml"
    file.write_text("""
database:
  host: localhost
  port: 5432
model:
  name: random_forest
  version: 1
""")
    return file


@pytest.fixture
def empty_yaml_file(tmp_path):
    """Creates a real temporary empty YAML file."""
    file = tmp_path / "empty.yaml"
    file.write_text("")
    return file


# ── tests ────────────────────────────────────────────────────────────────────

class TestReadYaml:

    def test_returns_config_box(self, valid_yaml_file):
        result = read_yaml(valid_yaml_file)
        assert isinstance(result, ConfigBox)

    def test_content_is_correct(self, valid_yaml_file):
        result = read_yaml(valid_yaml_file)
        assert result.database.host == "localhost"
        assert result.database.port == 5432
        assert result.model.name == "random_forest"

    def test_dot_notation_access(self, valid_yaml_file):
        """ConfigBox allows dot notation — verify it works."""
        result = read_yaml(valid_yaml_file)
        assert result.model.version == 1

    def test_empty_yaml_raises_value_error(self, empty_yaml_file):
        with pytest.raises(ValueError, match="yaml file is empty"):
            read_yaml(empty_yaml_file)

    def test_nonexistent_file_raises_exception(self, tmp_path):
        fake_path = tmp_path / "does_not_exist.yaml"
        with pytest.raises(Exception):
            read_yaml(fake_path)

    def test_wrong_type_raises_type_error(self):
        with pytest.raises(EnsureError):
            read_yaml("not_a_path_object")