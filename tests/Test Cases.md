# Test Case Documentation

## Overview

| Module | Class | Total Tests |
|---|---|---|
| `data_ingestion` | `DataIngestion` | 11 |
| `model_training` | `ModelTraining` | 12 |

---

## `DataIngestion` — `src/ds_e2e_project/components/data_ingestion.py`

### `__init__`

| ID | Test Name | Description | Expected Result |
|---|---|---|---|
| DI-001 | `test_config_is_assigned` | Config object passed to constructor is stored as `self.config` | `data_ingestion.config == mock_config` |
| DI-002 | `test_config_fields_accessible` | Fields on the stored config are readable | `source_URL` and `local_data_file` return correct values |

---

### `download_file`

| ID | Test Name | Description | Expected Result |
|---|---|---|---|
| DI-003 | `test_downloads_when_file_missing` | File does not exist locally — triggers download | `urlretrieve` called once with correct `url` and `filename` |
| DI-004 | `test_skips_download_when_file_exists` | File already exists locally — skips download | `urlretrieve` not called |
| DI-005 | `test_logs_on_successful_download` | Successful download emits a log entry | `logger.info` called once after download |
| DI-006 | `test_logs_when_file_already_exists` | File already exists — correct skip message logged | `logger.info` called with `"File already exists."` |
| DI-007 | `test_raises_on_download_failure` | Network error during download | `Exception("Network error")` propagates to caller |

---

### `extract_zip_file`

| ID | Test Name | Description | Expected Result |
|---|---|---|---|
| DI-008 | `test_creates_unzip_directory` | Extraction directory is created before unzipping | `os.makedirs` called with correct path and `exist_ok=True` |
| DI-009 | `test_extracts_to_correct_path` | Zip contents extracted to the configured `unzip_dir` | `extractall` called with `unzip_dir` path |
| DI-010 | `test_opens_correct_zip_file` | Correct zip file opened in read mode | `ZipFile` called with `local_data_file` and `"r"` |
| DI-011 | `test_raises_on_bad_zip` | Corrupted or invalid zip file raises an error | `zipfile.BadZipFile` propagates to caller |

---

## `ModelTraining` — `src/ds_e2e_project/components/model_training.py`

### `__init__`

| ID | Test Name | Description | Expected Result |
|---|---|---|---|
| MT-001 | `test_config_is_assigned` | Config object passed to constructor is stored as `self.config` | `model_training.config == mock_config` |
| MT-002 | `test_config_fields_accessible` | Hyperparameter and path fields on config are readable | `alpha`, `l1_ratio`, `random_state`, `target_column` return correct values |

---

### `train`

| ID | Test Name | Description | Expected Result |
|---|---|---|---|
| MT-003 | `test_reads_train_and_test_csv` | Both train and test CSV files are read from configured paths | `pd.read_csv` called twice with correct paths |
| MT-004 | `test_target_column_excluded_from_features` | Target column is dropped from feature matrix `X` | `"quality"` not present in columns passed to `fit` |
| MT-005 | `test_target_column_is_labels` | Target column is used as label vector `y` | DataFrame with only `"quality"` column passed as second arg to `fit` |
| MT-006 | `test_elasticnet_initialized_with_correct_params` | ElasticNet model created with `alpha`, `l1_ratio`, `random_state` from config | `ElasticNet(alpha=0.2, l1_ratio=0.1, random_state=42)` |
| MT-007 | `test_model_is_fitted` | `fit` is called on the ElasticNet instance | `ElasticNet.fit` called exactly once |
| MT-008 | `test_model_saved_to_correct_path` | Trained model is saved to `root_dir/model_name` | `joblib.dump` called with `artifacts/model_training/model.joblib` |
| MT-009 | `test_joblib_dump_called_once` | Model serialization happens exactly once per training run | `joblib.dump` call count equals 1 |
| MT-010 | `test_raises_when_train_csv_missing` | Training CSV file does not exist at configured path | `FileNotFoundError` propagates to caller |
| MT-011 | `test_raises_when_target_column_missing` | Target column absent from loaded DataFrame | `KeyError` propagates to caller |
| MT-012 | `test_raises_when_model_save_fails` | Disk write error during `joblib.dump` | `OSError` propagates to caller |
