import os
import logging
import sys

import click
from make_dataset.s3_storage import download_file

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


@click.command("download")
@click.option("--s3-bucket")
@click.option("--remote-path")
@click.option("--output-path")
def download_dataset(s3_bucket: str, remote_path: str, output_path: str):
    remote_path_demand_orders = f"{remote_path}/demand_orders.csv"
    output_local_path_demand_orders = f"{output_path}/demand_orders.csv"
    remote_path_demand_orders_status = f"{remote_path}/demand_orders_status.csv"
    output_local_path_demand_orders_status = f"{output_path}/demand_orders_status.csv"

    os.makedirs(output_path, exist_ok=True)
    # Download demand_orders.csv
    download_file(bucket_name=s3_bucket, remote_path=remote_path_demand_orders, local_path=output_local_path_demand_orders,)
    logger.info(f"remote_path: {remote_path}")
    logger.info(f"output_local_path: {output_local_path_demand_orders}")
    # Download demand_orders_status.csv
    download_file(bucket_name=s3_bucket, remote_path=remote_path_demand_orders_status, local_path=output_local_path_demand_orders_status,)
    logger.info(f"remote_path: {remote_path}")
    logger.info(f"output_local_path: {output_local_path_demand_orders_status}")


if __name__ == "__main__":
    download_dataset()
