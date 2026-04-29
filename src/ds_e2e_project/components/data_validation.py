import os
from src.ds_e2e_project import logger
from src.ds_e2e_project.entity.config_entity import (DataValidationConfig)
import pandas as pd

class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_all_columns(self) -> bool:
        try:
            data = pd.read_csv(self.config.unzip_data_dir)

            all_cols = list(data.columns)
            schema_cols = list(self.config.all_schema.keys())

            # Check column names match schema
            validation_status = True
            for col in all_cols:
                if col not in schema_cols:
                    validation_status = False
                    break

            # Check if all columns are numerical
            if validation_status:
                all_numeric = all(pd.api.types.is_numeric_dtype(data[col]) for col in all_cols)
                if not all_numeric:
                    validation_status = False

            # Write final status once
            with open(self.config.STATUS_FILE, 'w') as f:
                f.write(f"Validation status: {validation_status}")

            return validation_status

        except Exception as e:
            raise e