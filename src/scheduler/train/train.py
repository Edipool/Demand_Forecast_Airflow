import json
import logging
import os
import sys

import click
import pandas as pd
from src_demand_forecast.entities.train_pipeline_params import (TrainPipelineParams,
                                            read_training_pipeline_params)
from src_demand_forecast.models.train_model import (MultiTargetModel, evaluate_model,
                                      serialize_model)


logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


@click.command("train")
@click.option("--input-dir")
@click.option("--output-dir")
@click.option("--config")
def train(input_dir: str, output_dir: str, config: str):
    logger.info(f"input_dir: {input_dir}")
    logger.info(f"output_dir: {output_dir}")
    logger.info(f"config: {config}")

    os.makedirs(output_dir, exist_ok=True)

    training_pipeline_params: TrainPipelineParams = read_training_pipeline_params(
        config
    )
    dftrain = pd.read_csv(os.path.join(input_dir, "train.csv"))
    dftest = pd.read_csv(os.path.join(input_dir, "test.csv"))

    model = MultiTargetModel(features=training_pipeline_params.model_params.features)
    model.fit(dftrain)
    predictions = model.predict(dftest)
    # Save predictions to .csv
    logger.info("Saving predictions...")
    path_predictions = os.path.join(output_dir, "predictions.csv")
    predictions.to_csv(path_predictions, index=False)
    # Evaluate model
    logger.info("Evaluating model...")
    losses = evaluate_model(dftest, predictions)
    logger.info(f"Losses is {losses}")
    logger.info("Finish training model")
    # Save losses in dump .json
    path_losses = os.path.join(output_dir, "losses.json")
    with open(path_losses, "w") as file:
        json.dump(losses, file)
        logger.info("Losses saved successfully!")
    # Serialize model
    logger.info("Saving model...")
    path_model = os.path.join(output_dir, "model.pkl")
    serialize_model(model, path_model)
    logger.info("Model saved successfully!")


if __name__ == "__main__":
    train()
