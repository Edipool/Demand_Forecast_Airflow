import logging
import os
import sys
from datetime import datetime

import click
import pandas as pd
from entities.train_pipeline_params import (TrainPipelineParams,
                                            read_training_pipeline_params)
from features.build_sku_by_day import save_sku_demand_by_day, sku_demand_by_day
from features.build_transformer import (features_and_targets_transformer,
                                        save_transformed_data)

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

    os.makedirs(output_dir, exist_ok=True)

    training_pipeline_params: TrainPipelineParams = read_training_pipeline_params(
        config
    )
    logger.info(f"params: {training_pipeline_params}")
    demand_orders = pd.read_csv(os.path.join(input_dir, "demand_orders.csv"))
    demand_orders_status = pd.read_csv(
        os.path.join(input_dir, "demand_orders_status.csv")
    )
    # Make sku_demand_by_day
    logger.info("Start training...")
    logger.info("Make sku demand day...")
    sku_demand_day = sku_demand_by_day(demand_orders, demand_orders_status)
    # Save sku_demand_by_day
    logger.info("Saving sku demand day...")
    save_sku_demand_by_day_path = os.path.join(
        output_dir, f"sku_demand_day.csv")
    save_sku_demand_by_day(save_sku_demand_by_day_path, sku_demand_day)
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
    save_transformed_data_path = os.path.join(
        output_dir, "features_targets.csv"
    )
    print(f"save_path: {save_transformed_data_path}")
    save_transformed_data(save_transformed_data_path, transformed_data)


if __name__ == "__main__":
    preprocess()
