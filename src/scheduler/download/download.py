import logging
import os
import sys
import click

from demand_forecast_source.download.download_from_s3 import download_dataset

@click.command("download")
@click.option("--s3-bucket")
@click.option("--remote-path")
@click.option("--output-path")
def download(s3_bucket, remote_path, output_path):
    logging.info("Downloading dataset from S3")
    download_dataset(s3_bucket, remote_path, output_path)

if __name__ == "__main__":
    download()
