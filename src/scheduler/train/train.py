import json
import os
import logging
import sys
import pandas as pd
import click

from entities.train_pipeline_params import (
    TrainingPipelineParams,
    read_training_pipeline_params,
)
from models.model_fit_predict import (
    train_model,
    predict_model,
    evaluate_model,
    serialize_model,
)

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


# @click.command("train")
# @click.option("--input-dir")
# @click.option("--output-dir")
# @click.option("--config")
# def train(input_dir: str, output_dir: str, config: str):
