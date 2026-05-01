from src.ds_e2e_project.config.configuration import ConfigurationManager
from src.ds_e2e_project.components.model_training import ModelTraining


STAGE_NAME = "Model Training stage"

class ModelTrainingPipeline:
    def __init__(self):
        pass
    def initiate_model_training_(self):
        config = ConfigurationManager()
        model_training_config = config.get_model_training_config()
        model_training = ModelTraining(config = model_training_config)
        model_training.train()
