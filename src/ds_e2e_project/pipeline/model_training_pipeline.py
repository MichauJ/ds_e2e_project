from src.ds_e2e_project.config.configuration import ConfigurationManager
from src.ds_e2e_project.entity.config_entity import ModelTrainingConfig
from src.ds_e2e_project.components.model_training import ModelTraining
from src.ds_e2e_project import logger

STAGE_NAME = "Model Training stage"

class ModelTrainingPipeline:
    def __init__(self):
        pass
    def initiate_model_training_(self):
        config = ConfigurationManager()
        model_training_config = config.get_model_training_config()
        model_training = ModelTraining(config = model_training_config)
        model_training.train()
