import os

import airflow
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
from dotenv import load_dotenv

load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

with DAG(
    dag_id="airflow_download_data_from_s3",
    start_date=airflow.utils.dates.days_ago(1),
    schedule_interval="@daily",
) as dag:

    get_data = DockerOperator(
        image="download",
        command="--s3-bucket regsys --remote-path 2023-09-27 --output-path data/raw",
        task_id="download",
        do_xcom_push=False,
        environment={
            "AWS_ACCESS_KEY_ID": AWS_ACCESS_KEY_ID,
            "AWS_SECRET_ACCESS_KEY": AWS_SECRET_ACCESS_KEY,
        },
        mounts=[
            Mount(
                source=f"{os.environ['DATA_VOLUME_PATH']}/data",
                target="/data",
                type="bind",
            )
        ],
    )

    notify = BashOperator(
        task_id="notify", bash_command=f"echo new rows of data generated ...",
    )

    get_data >> notify
