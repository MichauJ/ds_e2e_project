# tests/unit/test_common.py

import pytest
from pathlib import Path
from box import ConfigBox
from ensure import EnsureError
from ds_e2e_project.utils.common import read_yaml
import os
import pytest
from pathlib import Path
from box import ConfigBox
from ensure import EnsureError

from ds_e2e_project.utils.common import create_directories, save_json, load_json


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




# ── create_directories ───────────────────────────────────────────────────────

class TestCreateDirectories:

    def test_creates_single_directory(self, tmp_path):
        new_dir = tmp_path / "new_folder"
        create_directories([new_dir])
        assert os.path.isdir(new_dir)

    def test_creates_multiple_directories(self, tmp_path):
        dirs = [tmp_path / "folder1", tmp_path / "folder2", tmp_path / "folder3"]
        create_directories(dirs)
        for d in dirs:
            assert os.path.isdir(d)

    def test_does_not_fail_if_directory_exists(self, tmp_path):
        existing = tmp_path / "already_exists"
        existing.mkdir()
        create_directories([existing])   # exist_ok=True — should not raise
        assert os.path.isdir(existing)

    def test_creates_nested_directories(self, tmp_path):
        nested = tmp_path / "parent" / "child" / "grandchild"
        create_directories([nested])
        assert os.path.isdir(nested)

    def test_wrong_type_raises_ensure_error(self):
        with pytest.raises(EnsureError):
            create_directories("not_a_list")  # str instead of list


# ── save_json ────────────────────────────────────────────────────────────────

class TestSaveJson:

    def test_file_is_created(self, tmp_path):
        path = tmp_path / "data.json"
        save_json(path, {"key": "value"})
        assert path.exists()

    def test_content_is_correct(self, tmp_path):
        import json
        path = tmp_path / "data.json"
        data = {"name": "alice", "score": 42}
        save_json(path, data)
        with open(path) as f:
            loaded = json.load(f)
        assert loaded == data

    def test_saves_nested_dict(self, tmp_path):
        import json
        path = tmp_path / "nested.json"
        data = {"model": {"name": "rf", "params": {"n_estimators": 100}}}
        save_json(path, data)
        with open(path) as f:
            loaded = json.load(f)
        assert loaded["model"]["params"]["n_estimators"] == 100

    def test_wrong_path_type_raises_ensure_error(self):
        with pytest.raises(EnsureError):
            save_json("not_a_path", {"key": "value"})  # str instead of Path

    def test_wrong_data_type_raises_ensure_error(self, tmp_path):
        path = tmp_path / "data.json"
        with pytest.raises(EnsureError):
            save_json(path, ["not", "a", "dict"])  # list instead of dict


# ── load_json ────────────────────────────────────────────────────────────────

class TestLoadJson:

    @pytest.fixture
    def json_file(self, tmp_path):
        """Creates a temporary JSON file with content."""
        import json
        path = tmp_path / "data.json"
        data = {"database": {"host": "localhost", "port": 5432}}
        with open(path, "w") as f:
            json.dump(data, f)
        return path

    def test_returns_config_box(self, json_file):
        result = load_json(json_file)
        assert isinstance(result, ConfigBox)

    def test_content_is_correct(self, json_file):
        result = load_json(json_file)
        assert result.database.host == "localhost"
        assert result.database.port == 5432

    def test_dot_notation_access(self, json_file):
        result = load_json(json_file)
        assert result.database.host == "localhost"  # dot notation, not ["host"]

    def test_nonexistent_file_raises_exception(self, tmp_path):
        fake_path = tmp_path / "does_not_exist.json"
        with pytest.raises(Exception):
            load_json(fake_path)

    def test_wrong_type_raises_ensure_error(self):
        with pytest.raises(EnsureError):
            load_json("not_a_path")  # str instead of Path