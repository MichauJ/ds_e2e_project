import os
import zipfile
import pytest
from unittest.mock import patch, MagicMock, mock_open
from src.ds_e2e_project.components.data_ingestion import DataIngestion
from src.ds_e2e_project.entity.config_entity import DataIngestionConfig


@pytest.fixture
def mock_config():
    return DataIngestionConfig(
        root_dir="artifacts/data_ingestion",
        source_URL="https://example.com/data.zip",
        local_data_file="artifacts/data_ingestion/data.zip",
        unzip_dir="artifacts/data_ingestion/unzipped"
    )


@pytest.fixture
def data_ingestion(mock_config):
    return DataIngestion(config=mock_config)


# ─── __init__ ────────────────────────────────────────────────────────────────

class TestDataIngestionInit:
    def test_config_is_assigned(self, data_ingestion, mock_config):
        assert data_ingestion.config == mock_config

    def test_config_fields_accessible(self, data_ingestion):
        assert data_ingestion.config.source_URL == "https://example.com/data.zip"
        assert data_ingestion.config.local_data_file == "artifacts/data_ingestion/data.zip"


# ─── download_file ────────────────────────────────────────────────────────────

class TestDownloadFile:
    @patch("src.ds_e2e_project.components.data_ingestion.request.urlretrieve")
    @patch("os.path.exists", return_value=False)
    def test_downloads_when_file_missing(self, mock_exists, mock_urlretrieve, data_ingestion):
        mock_urlretrieve.return_value = ("artifacts/data_ingestion/data.zip", {"Content-Type": "application/zip"})

        data_ingestion.download_file()

        mock_urlretrieve.assert_called_once_with(
            url="https://example.com/data.zip",
            filename="artifacts/data_ingestion/data.zip"
        )

    @patch("src.ds_e2e_project.components.data_ingestion.request.urlretrieve")
    @patch("os.path.exists", return_value=True)
    def test_skips_download_when_file_exists(self, mock_exists, mock_urlretrieve, data_ingestion):
        data_ingestion.download_file()

        mock_urlretrieve.assert_not_called()

    @patch("src.ds_e2e_project.components.data_ingestion.request.urlretrieve")
    @patch("os.path.exists", return_value=False)
    def test_logs_on_successful_download(self, mock_exists, mock_urlretrieve, data_ingestion):
        mock_urlretrieve.return_value = ("data.zip", "some-header-info")

        with patch("src.ds_e2e_project.components.data_ingestion.logger") as mock_logger:
            data_ingestion.download_file()
            mock_logger.info.assert_called_once()

    @patch("src.ds_e2e_project.components.data_ingestion.request.urlretrieve")
    @patch("os.path.exists", return_value=True)
    def test_logs_when_file_already_exists(self, mock_exists, mock_urlretrieve, data_ingestion):
        with patch("src.ds_e2e_project.components.data_ingestion.logger") as mock_logger:
            data_ingestion.download_file()
            mock_logger.info.assert_called_with("File already exists.")

    @patch("src.ds_e2e_project.components.data_ingestion.request.urlretrieve", side_effect=Exception("Network error"))
    @patch("os.path.exists", return_value=False)
    def test_raises_on_download_failure(self, mock_exists, mock_urlretrieve, data_ingestion):
        with pytest.raises(Exception, match="Network error"):
            data_ingestion.download_file()


# ─── extract_zip_file ─────────────────────────────────────────────────────────

class TestExtractZipFile:
    @patch("zipfile.ZipFile")
    @patch("os.makedirs")
    def test_creates_unzip_directory(self, mock_makedirs, mock_zipfile, data_ingestion):
        mock_zipfile.return_value.__enter__ = MagicMock(return_value=MagicMock())
        mock_zipfile.return_value.__exit__ = MagicMock(return_value=False)

        data_ingestion.extract_zip_file()

        mock_makedirs.assert_called_once_with("artifacts/data_ingestion/unzipped", exist_ok=True)

    @patch("zipfile.ZipFile")
    @patch("os.makedirs")
    def test_extracts_to_correct_path(self, mock_makedirs, mock_zipfile, data_ingestion):
        mock_zip_ref = MagicMock()
        mock_zipfile.return_value.__enter__ = MagicMock(return_value=mock_zip_ref)
        mock_zipfile.return_value.__exit__ = MagicMock(return_value=False)

        data_ingestion.extract_zip_file()

        mock_zip_ref.extractall.assert_called_once_with("artifacts/data_ingestion/unzipped")

    @patch("zipfile.ZipFile")
    @patch("os.makedirs")
    def test_opens_correct_zip_file(self, mock_makedirs, mock_zipfile, data_ingestion):
        mock_zip_ref = MagicMock()
        mock_zipfile.return_value.__enter__ = MagicMock(return_value=mock_zip_ref)
        mock_zipfile.return_value.__exit__ = MagicMock(return_value=False)

        data_ingestion.extract_zip_file()

        mock_zipfile.assert_called_once_with("artifacts/data_ingestion/data.zip", "r")

    @patch("zipfile.ZipFile", side_effect=zipfile.BadZipFile("Bad zip"))
    @patch("os.makedirs")
    def test_raises_on_bad_zip(self, mock_makedirs, mock_zipfile, data_ingestion):
        with pytest.raises(zipfile.BadZipFile):
            data_ingestion.extract_zip_file()