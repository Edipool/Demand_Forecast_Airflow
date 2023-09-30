import logging
import sys
from dataclasses import dataclass, field

import yaml
from entities.train_params import ModelParams
from marshmallow_dataclass import class_schema

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


PATH = "../configs/train_config.yaml"


@dataclass()
class TrainingPipelineParams:
    model_params: ModelParams
    output_predictions: str = field(default="data/predictions/predictions.csv")
    output_losses: str = field(default="models/losses.json")
    output_model: str = field(default="models/model.pkl")


TrainingPipelineParamsSchema = class_schema(TrainingPipelineParams)


def read_training_pipeline_params(path: str) -> TrainingPipelineParams:
    with open(path, "r") as input_stream:
        config_dict = yaml.safe_load(input_stream)
        schema = TrainingPipelineParamsSchema().load(config_dict)
        logger.info("Check schema: %s", schema)
        return schema
