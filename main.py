from src.ds_e2e_project import logger
from src.ds_e2e_project.pipeline.data_ingestion_pipeline import DataIngestionTrainingPipeline
from src.ds_e2e_project.pipeline.data_validation_pipeline import DataValidationTrainingPipeline
from src.ds_e2e_project.pipeline.data_transformation_pipeline import DataTransformationTrainingPipeline
from src.ds_e2e_project.pipeline.model_training_pipeline import ModelTrainingPipeline
from src.ds_e2e_project.pipeline.model_evaluation_pipeline import ModelEvaluationPipeline
STAGE_NAME = "Data Ingestion Stage"

try:
        logger.info(f">>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataIngestionTrainingPipeline()
        obj.initiate_data_ingestion()
        logger.info(f">>>> stage {STAGE_NAME} completed <<<<<<< \n\nx================x")
except Exception as e:
         logger.exception(e)
         raise e
STAGE_NAME = "Data Validation Stage"
try:
    logger.info(f">>>>> stage {STAGE_NAME} started <<<<<<")
    obj = DataValidationTrainingPipeline()
    obj.initiate_data_validation()
    logger.info(f">>>> stage {STAGE_NAME} completed <<<<<<< \n\nx================x")
except Exception as e:
         
         logger.exception(e)
         raise e
STAGE_NAME = "Data Transformation Stage"
try:
    logger.info(f">>>>> stage {STAGE_NAME} started <<<<<<")
    obj = DataTransformationTrainingPipeline()
    obj.initiate_data_transformation()
    logger.info(f">>>> stage {STAGE_NAME} completed <<<<<<< \n\nx================x")
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME = "Model Training stage"
try:
    logger.info(f">>>>> stage {STAGE_NAME} started <<<<<<")
    obj = ModelTrainingPipeline()
    obj.initiate_model_training_()
    logger.info(f">>>> stage {STAGE_NAME} completed <<<<<<< \n\nx================x")
except Exception as e:
         logger.exception(e)
         raise e

STAGE_NAME = "Model Evaluation stage"
try:
    logger.info(f">>>>> stage {STAGE_NAME} started <<<<<<")
    obj = ModelEvaluationPipeline()
    obj.initiate_model_evaluation_()
    logger.info(f">>>> stage {STAGE_NAME} completed <<<<<<< \n\nx================x")
except Exception as e:
         logger.exception(e)
         raise e

def main():
    print("Hello from ds-e2e-project!")


if __name__ == "__main__":
    main()
