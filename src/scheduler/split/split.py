import os
import logging
import sys
import click
from make_dataset.make_dataset import read_data, split_train_test

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


@click.command("split")
@click.option("--input-dir")
@click.option("--output-dir")
@click.option("--test_days")
def split(input_dir: str, output_dir: str, test_days: int):
    logger.info(f"input_dir: {input_dir}")
    logger.info(f"output_dir: {output_dir}")
    logger.info(f"test_size: {test_days}")

    os.makedirs(output_dir, exist_ok=True)

    df = read_data(os.path.join(input_dir, "features_targets.csv"))

    train, test = split_train_test(df, test_days=int(test_days))

    train.to_csv(os.path.join(output_dir, "train.csv"), index=False)
    test.to_csv(os.path.join(output_dir, "test.csv"), index=False)
    logger.info(f"Split data complete!")


if __name__ == "__main__":
    split()
