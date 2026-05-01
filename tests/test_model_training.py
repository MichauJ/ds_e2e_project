import os
import pytest
import numpy as np
import pandas as pd
import joblib
from unittest.mock import patch, MagicMock
from src.ds_e2e_project.components.model_training import ModelTraining
from src.ds_e2e_project.entity.config_entity import ModelTrainingConfig


@pytest.fixture
def mock_config():
    return ModelTrainingConfig(
        root_dir="artifacts/model_training",
        train_data_path="artifacts/data/train.csv",
        test_data_path="artifacts/data/test.csv",
        model_name="model.joblib",
        alpha=0.2,
        l1_ratio=0.1,
        random_state=42,
        target_column="quality"
    )


@pytest.fixture
def model_training(mock_config):
    return ModelTraining(config=mock_config)


@pytest.fixture
def mock_train_df():
    return pd.DataFrame({
        "feature_1": [1.0, 2.0, 3.0, 4.0, 5.0],
        "feature_2": [0.5, 1.5, 2.5, 3.5, 4.5],
        "quality":   [5,   6,   7,   6,   8  ]
    })


@pytest.fixture
def mock_test_df():
    return pd.DataFrame({
        "feature_1": [1.5, 2.5],
        "feature_2": [0.8, 1.8],
        "quality":   [5,   7  ]
    })


# ─── __init__ ─────────────────────────────────────────────────────────────────

class TestModelTrainingInit:
    def test_config_is_assigned(self, model_training, mock_config):
        assert model_training.config == mock_config

    def test_config_fields_accessible(self, model_training):
        assert model_training.config.alpha == 0.2
        assert model_training.config.l1_ratio == 0.1
        assert model_training.config.random_state == 42
        assert model_training.config.target_column == "quality"


# ─── train ────────────────────────────────────────────────────────────────────

class TestModelTrainingTrain:
    @patch("joblib.dump")
    @patch("pandas.read_csv")
    def test_reads_train_and_test_csv(self, mock_read_csv, mock_dump, model_training, mock_train_df, mock_test_df):
        mock_read_csv.side_effect = [mock_train_df, mock_test_df]

        model_training.train()

        assert mock_read_csv.call_count == 2
        calls = [c.args[0] for c in mock_read_csv.call_args_list]
        assert "artifacts/data/train.csv" in calls
        assert "artifacts/data/test.csv" in calls

    @patch("joblib.dump")
    @patch("pandas.read_csv")
    def test_target_column_excluded_from_features(self, mock_read_csv, mock_dump, model_training, mock_train_df, mock_test_df):
        mock_read_csv.side_effect = [mock_train_df, mock_test_df]

        with patch("sklearn.linear_model.ElasticNet.fit") as mock_fit:
            model_training.train()
            train_x_used = mock_fit.call_args[0][0]
            assert "quality" not in train_x_used.columns

    @patch("joblib.dump")
    @patch("pandas.read_csv")
    def test_target_column_is_labels(self, mock_read_csv, mock_dump, model_training, mock_train_df, mock_test_df):
        mock_read_csv.side_effect = [mock_train_df, mock_test_df]

        with patch("sklearn.linear_model.ElasticNet.fit") as mock_fit:
            model_training.train()
            train_y_used = mock_fit.call_args[0][1]
            assert list(train_y_used.columns) == ["quality"]

    @patch("joblib.dump")
    @patch("pandas.read_csv")
    def test_elasticnet_initialized_with_correct_params(self, mock_read_csv, mock_dump, model_training, mock_train_df, mock_test_df):
        mock_read_csv.side_effect = [mock_train_df, mock_test_df]

        with patch("src.ds_e2e_project.components.model_training.ElasticNet") as mock_en:
            mock_en.return_value.fit = MagicMock()
            model_training.train()
            mock_en.assert_called_once_with(alpha=0.2, l1_ratio=0.1, random_state=42)

    @patch("joblib.dump")
    @patch("pandas.read_csv")
    def test_model_is_fitted(self, mock_read_csv, mock_dump, model_training, mock_train_df, mock_test_df):
        mock_read_csv.side_effect = [mock_train_df, mock_test_df]

        with patch("sklearn.linear_model.ElasticNet.fit") as mock_fit:
            model_training.train()
            mock_fit.assert_called_once()

    @patch("joblib.dump")
    @patch("pandas.read_csv")
    def test_model_saved_to_correct_path(self, mock_read_csv, mock_dump, model_training, mock_train_df, mock_test_df):
        mock_read_csv.side_effect = [mock_train_df, mock_test_df]

        model_training.train()

        saved_path = mock_dump.call_args[0][1]
        assert saved_path == os.path.join("artifacts/model_training", "model.joblib")

    @patch("joblib.dump")
    @patch("pandas.read_csv")
    def test_joblib_dump_called_once(self, mock_read_csv, mock_dump, model_training, mock_train_df, mock_test_df):
        mock_read_csv.side_effect = [mock_train_df, mock_test_df]

        model_training.train()

        mock_dump.assert_called_once()

    @patch("pandas.read_csv", side_effect=FileNotFoundError("train.csv not found"))
    def test_raises_when_train_csv_missing(self, mock_read_csv, model_training):
        with pytest.raises(FileNotFoundError, match="train.csv not found"):
            model_training.train()

    @patch("pandas.read_csv")
    def test_raises_when_target_column_missing(self, mock_read_csv, model_training):
        bad_df = pd.DataFrame({"feature_1": [1.0, 2.0], "feature_2": [0.5, 1.5]})  # no "quality"
        mock_read_csv.side_effect = [bad_df, bad_df]

        with pytest.raises(KeyError):
            model_training.train()

    @patch("joblib.dump", side_effect=OSError("Disk write failed"))
    @patch("pandas.read_csv")
    def test_raises_when_model_save_fails(self, mock_read_csv, mock_dump, model_training, mock_train_df, mock_test_df):
        mock_read_csv.side_effect = [mock_train_df, mock_test_df]

        with pytest.raises(OSError, match="Disk write failed"):
            model_training.train()