import pendulum

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime, timedelta


default_args = {
    "retries": 3,
    "retry_delay": timedelta(seconds=10),
}

with DAG(
    dag_id="de_exam",
    start_date=pendulum.datetime(2025, 6, 15, tz="UTC"),
    schedule="@daily",
    catchup=False,
    tags=["de"],
    default_args=default_args,
) as dag:

    fetch = DockerOperator(
        task_id="fetch",
        image="de-exam-dag",
        command="python3 src/etl/fetch.py",
        do_xcom_push=True,
        skip_on_exit_code=99,
    )
    # eda
    # train
    # export

# fetch >> eda >> train >> export
