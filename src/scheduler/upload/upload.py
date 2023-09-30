import logging
import sys

import click
from send_dataset.s3_storage import upload_file

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


@click.command("upload")
@click.option("--output-path")
@click.option("--s3-bucket")
@click.option("--remote_path")
def upload_dataset(output_path: str, s3_bucket: str, remote_path: str):
    upload_file(output_path, s3_bucket, remote_path)


if __name__ == "__main__":
    upload_dataset()
