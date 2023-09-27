import yaml
import logging
import sys

from dataclasses import dataclass, field
from marshmallow_dataclass import class_schema

from entities.train_params import ModelParams


logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


PATH = "../configs/train_config.yaml"


@dataclass()
class TrainingPipelineParams:
    output_model_path: str
    metric_path: str
    train_params: ModelParams
    input_data_path: str = field(default="../data/raw/demand_orders.csv")
    input_preprocessed_data_path: str = field(
        default="../data/raw/demand_orders_status.csv"
    )


TrainingPipelineParamsSchema = class_schema(TrainingPipelineParams)


def read_training_pipeline_params(path: str) -> TrainingPipelineParams:
    with open(path, "r") as input_stream:
        config_dict = yaml.safe_load(input_stream)
        schema = TrainingPipelineParamsSchema().load(config_dict)
        logger.info("Check schema: %s", schema)
        return schema
