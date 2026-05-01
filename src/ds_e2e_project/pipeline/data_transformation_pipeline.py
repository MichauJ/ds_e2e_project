from src.ds_e2e_project.config.configuration import ConfigurationManager
from src.ds_e2e_project.entity.config_entity import (DataTransformationConfig)
from src.ds_e2e_project.components.data_transformation import DataTransformation
from src.ds_e2e_project import logger
from pathlib import Path

STAGE_NAME = "Data Transformation stage"

class DataTransformationTrainingPipeline:
    def __init__(self):
        pass
    def initiate_data_transformation(self):
        try:
            with open(Path("artifacts/data_validation/status.txt"),'r') as f:
                status = f.read().split(" ")[-1]
            if status == "True":
                config = ConfigurationManager()
                data_transformation_config = config.get_data_transformation_config()
                data_transformation = DataTransformation(config=data_transformation_config)
                data_transformation.train_test_splitting()
            else:
                raise Exception("The data scheme is invalid")
        except Exception as e:
            print(e)