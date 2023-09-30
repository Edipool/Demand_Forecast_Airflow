import os

import airflow
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.sensors.filesystem import FileSensor
from docker.types import Mount

with DAG(
    dag_id="airflow_train_val",
    start_date=airflow.utils.dates.days_ago(1),
    schedule_interval="@daily",
) as dag:
    wait_for_data = FileSensor(
        task_id="wait-for-data",
        poke_interval=5,
        retries=5,
        filepath="data/raw/demand_orders.csv",
    )

    wait_for_another_table = FileSensor(
        task_id="wait-for-another-table",
        poke_interval=5,
        retries=5,
        filepath="data/raw/demand_orders_status.csv",
    )

    preprocess = DockerOperator(
        image="preprocess",
        command="--input-dir data/raw --output-dir data/processed --config configs/train_config.yaml",
        task_id="preprocess",
        do_xcom_push=False,
        mounts=[
            Mount(
                source=f"{os.environ['DATA_VOLUME_PATH']}/data",
                target="/data",
                type="bind",
            )
        ],
    )

    split = DockerOperator(
        image="split",
        command="--input-dir data/processed --output-dir data/processed --test_days 30",
        task_id="split",
        do_xcom_push=False,
        mounts=[
            Mount(
                source=f"{os.environ['DATA_VOLUME_PATH']}/data",
                target="/data",
                type="bind",
            )
        ],
    )

    train = DockerOperator(
        image="train",
        command="--input-dir data/processed --output-dir data/predictions --config configs/train_config.yaml",
        task_id="train",
        do_xcom_push=False,
        mounts=[
            Mount(
                source=f"{os.environ['DATA_VOLUME_PATH']}/data",
                target="/data",
                type="bind",
            )
        ],
    )

    notify = BashOperator(
        task_id="notify", bash_command=f'echo "Model train and validated ... "',
    )

    wait_for_data >> preprocess >> split >> train >> notify