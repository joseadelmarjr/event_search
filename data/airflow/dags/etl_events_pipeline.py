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


def get_ticketmaster_events():
    from ingestor.TicketMaster import TicketMasterApi

    start_data_str = "2023-03-10"
    end_data_str = "2023-03-17"

    start_datetime = datetime.strptime(start_data_str, "%Y-%m-%d")
    end_datetime = datetime.strptime(end_data_str, "%Y-%m-%d")

    ticket_master = TicketMasterApi(start_datetime, end_datetime)

    while not ticket_master.is_finished():
        ticket_master.get_events()
        ticket_master.save_events()
        ticket_master.next_page()


def get_sympla_crawler():
    from ingestor.crawler.sympla import SymplaCrawler

    sympla_crawler = SymplaCrawler()

    print(sympla_crawler.is_finished())

    while not sympla_crawler.is_finished():
        sympla_crawler.get_events()
        sympla_crawler.save_events()
        sympla_crawler.next_page()    

with DAG(
    dag_id="etl_events_pipeline",
    default_args=dag_parameters,
    description="Dag responsable from get event to any sources and save to datalake.",
    tags=["land", "ticket_master"],
    schedule="5 * * * *",
) as dag:
    start_pipeline = EmptyOperator(task_id="start_pipeline")

    get_ticketmaster_events = PythonOperator(
        task_id="get_ticketmaster_events",
        python_callable=get_ticketmaster_events,
    )

    get_sympla_crawler = PythonOperator(
        task_id="get_sympla_crawler",
        python_callable=get_sympla_crawler,
    )


    end_pipeline = EmptyOperator(task_id="end_pipeline")

    # Orchestration
    start_pipeline >> get_ticketmaster_events
    start_pipeline >> get_sympla_crawler
    get_ticketmaster_events >> end_pipeline
    get_sympla_crawler >> end_pipeline
