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
    MultiTargetModel,
    evaluate_model,
    serialize_model,
)

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

    training_pipeline_params: TrainingPipelineParams = read_training_pipeline_params(
        config
    )
    dftrain = pd.read_csv(os.path.join(input_dir, "train.csv"))
    dftest = pd.read_csv(os.path.join(input_dir, "test.csv"))

    model = MultiTargetModel(features=training_pipeline_params.model_params.features)
    model.fit(dftrain)
    predictions = model.predict(dftest)
    # Save predictions to .csv
    logger.info("Saving predictions...")
    predictions.to_csv(training_pipeline_params.output_predictions, index=False)
    # Evaluate model
    logger.info("Evaluating model...")
    losses = evaluate_model(dftest, predictions)
    logger.info(f"Losses is {losses}")
    logger.info("Finish training model")
    # Save losses in dump .json
    with open(training_pipeline_params.output_losses, "w") as file:
        json.dump(losses, file)
    # Serialize model
    logger.info("Saving model...")
    serialize_model(model, training_pipeline_params.output_model)
    logger.info("Model saved successfully!")

if __name__ == "__main__":
    train()