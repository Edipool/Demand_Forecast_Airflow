import logging
import os
import sys

import click
from make_dataset.s3_storage import download_file

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


def download_and_log(
    s3_bucket: str, remote_path: str, output_path: str, file_name: str
):
    remote_file_path = f"{remote_path}/{file_name}"
    output_local_path = f"{output_path}/{file_name}"

    download_file(
        bucket_name=s3_bucket,
        remote_path=remote_file_path,
        local_path=output_local_path,
    )
    logger.info(f"remote_path: {remote_file_path}")
    logger.info(f"output_local_path: {output_local_path}")


@click.command("download")
@click.option("--s3-bucket")
@click.option("--remote-path")
@click.option("--output-path")
def download_dataset(s3_bucket: str, remote_path: str, output_path: str):
    os.makedirs(output_path, exist_ok=True)
    # Download demand_orders.csv and demand_orders_status.csv
    download_and_log(s3_bucket, remote_path, output_path, "demand_orders.csv")
    download_and_log(s3_bucket, remote_path, output_path, "demand_orders_status.csv")


if __name__ == "__main__":
    download_dataset()
