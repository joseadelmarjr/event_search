from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

dag_parameters = {
    "0wner": "airflow",
    "start_date": datetime(2023, 2, 3),
    "catchup": False,
}

# Parameters
THIS_PARAM_IS_EXAMPLE = "dag variable"


def python_task_function(param_function):
    __python_helper_function()
    return f"{THIS_PARAM_IS_EXAMPLE} and {param_function}"


def __python_helper_function():
    pass


with DAG(
    dag_id="dag_template",
    default_args=dag_parameters,
    description="Dag template V1",
    tags=["example_tag", "dag_template"],
    schedule="@once",
) as dag:
    start_pipeline = EmptyOperator(task_id="start_pipeline")

    python_task_example = PythonOperator(
        task_id="python_task_example",
        python_callable=python_task_function,
        op_args=["function variable"],
    )

    end_pipeline = EmptyOperator(task_id="end_pipeline")

    # Orchestration
    start_pipeline >> python_task_example
    python_task_example >> end_pipeline
