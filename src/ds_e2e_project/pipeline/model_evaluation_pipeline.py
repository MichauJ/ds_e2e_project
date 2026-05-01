from src.ds_e2e_project.config.configuration import ConfigurationManager
from src.ds_e2e_project.components.model_evaluation import ModelEvaluation


STAGE_NAME = "Model evaluation stage"

class ModelEvaluationPipeline:
    def __init__(self):
        pass
    def initiate_model_evaluation_(self):
        config = ConfigurationManager()
        model_evaluation_config = config.get_model_evaluation_config()
        model_evaluation = ModelEvaluation(config = model_evaluation_config)
        model_evaluation.log_into_mlflow()