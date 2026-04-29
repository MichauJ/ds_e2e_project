from src.ds_e2e_project.config.configuration import ConfigurationManager
from src.ds_e2e_project.entity.config_entity import (DataIngestionConfig)
from src.ds_e2e_project.components.data_ingestion import DataIngestion
from src.ds_e2e_project import logger

STAGE_NAME = "Data Ingestion Stage"

class DataIngestionTrainingPipeline:
    def __init__(self) -> None:
        pass
    def initiate_data_ingestion(self):
            config = ConfigurationManager()
            data_ingestion_config = config.get_data_ingestion_config()
            data_ingestion = DataIngestion(config=data_ingestion_config)
            data_ingestion.download_file()
            data_ingestion.extract_zip_file()

if __name__ == '__main__':
    try:
        logger.info(f">>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataIngestionTrainingPipeline()
        obj.initiate_data_ingestion()
        logger.info(f">>>> stage {STAGE_NAME} completed <<<<<<< \n\nx================x")
    except Exception as e:
         logger.exception(e)
         raise e