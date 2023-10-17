import logging
import sys

import click
from src_demand_forecast.upload.s3_storage import upload_dataset

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


@click.command("upload")
@click.option("--output-path")
@click.option("--s3-bucket")
@click.option("--remote_path")
def upload_to_s3(output_path: str, s3_bucket: str, remote_path: str):
    upload_dataset(output_path, s3_bucket, remote_path)


if __name__ == "__main__":
    upload_to_s3()
