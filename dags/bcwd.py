from datetime import timedelta

import pendulum
from airflow import DAG
from airflow.sdk import Variable
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

# The DAG configuration is stored in airflow variable
CONFIG = Variable.get('bcwd_config', deserialize_json=True)

default_args = {
    "retries": CONFIG.get('retries', 3),
    "retry_delay": timedelta(seconds=CONFIG.get('retry_delay', 10)),
    "mounts": [
        Mount(
            source=CONFIG.get('mount_source', "/hdd"),
            target=CONFIG.get('mount_target', "/hdd"),
            type="bind"
        ),
    ],
    'environment': CONFIG,
}

with DAG(
    dag_id="de_exam",
    start_date=pendulum.datetime(2025, 6, 15, tz="UTC"),
    schedule="@daily",
    catchup=False,
    tags=["de"],
    default_args=default_args,
    description="Breast Cancer Wisconsin",
) as dag:

    fetch = DockerOperator(
        task_id="fetch",
        image="de-exam-dag",
        command="python3 src/etl/fetch.py",
        do_xcom_push=True,
        skip_on_exit_code=99,
    )

    load = DockerOperator(
        task_id="load",
        image="de-exam-dag",
        command="python3 src/etl/load.py",
        do_xcom_push=True,
        trigger_rule="none_failed",
    )

    train = DockerOperator(
        task_id="train",
        image="de-exam-dag",
        command="python3 src/etl/train.py",
        do_xcom_push=True,
        trigger_rule="none_failed",
    )

fetch >> load >> train
