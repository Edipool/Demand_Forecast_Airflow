import os
import logging
import sys
import pandas as pd
import click
from datetime import datetime

from src.scheduler.preprocess.entities.train_pipeline_params import (
    TrainPipelineParams,
    read_training_pipeline_params,
)

from features.build_transformer import (features_and_targets_transformer)
from features.build_sku_by_day import save_sku_demand_by_day, sku_demand_by_day
from features.build_transformer import (features_and_targets_transformer,save_transformed_data)

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


@click.command("preprocess")
@click.option("--input-dir")
@click.option("--output-dir")
@click.option("--config")
def preprocess(input_dir: str, output_dir: str, config: str):
    logger.info(f"input_dir: {input_dir}")
    logger.info(f"output_dir: {output_dir}")
    logger.info(f"config: {config}")

    params = read_training_pipeline_params(config)
    logger.info(f"params: {params}")
    demand_orders = pd.read_csv(params.input_demand_orders)
    demand_orders_status = pd.read_csv(params.input_demand_orders_status)
    # Make sku_demand_by_day
    logger.info("Start training...")
    logger.info("Make sku demand day...")
    sku_demand_day = sku_demand_by_day(demand_orders, demand_orders_status)
    # Save sku_demand_by_day
    logger.info("Saving sku demand day...")
    save_sku_demand_by_day(params.output_sku_demand_day, sku_demand_day)
    logger.info("Sku demand day received successfully!")

    # Make features and targets transformer
    logger.info("Make transformer...")
    transformer = features_and_targets_transformer()
    # Transform data
    logger.info("Transforming data...")
    transformed_data = transformer.fit_transform(sku_demand_day)
    logger.info("Complete!")
    # Save transformed data
    logger.info("Saving transformed data...")
    save_transformed_data(params.output_features_and_targets, transformed_data)


if __name__ == "__main__":
    preprocess()
