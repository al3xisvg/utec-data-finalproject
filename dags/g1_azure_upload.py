from airflow.decorators import dag, task
from pendulum import datetime, timezone
import logging, time

from services.azurecli import Azure

from config.app import Config

log = logging.getLogger('airflow.task')


"""
Begin - Test
"""
def test():
    config = Config()

    azure_service = Azure(config=config)

    origin_path = "dags/g1_azure_upload.txt"
    target_path = "test/g1_azure_upload.txt"
    azure_service.upload_to_adls(
        origin_path = origin_path,
        target_path = target_path
    )
"""
End - Test
"""

@dag(
    dag_id="ssh_azure_upload_dag",
    description="DAG para subir archivos a Azure sando Service Principal",
    start_date=datetime(2025, 1, 1, tz=timezone("America/Lima")),
    schedule=None,
    catchup=False,
    tags=["config"],
)
def ssh_azure_upload_dag():

    @task
    def ssh_azure_upload():
        print("-------------------------------------------------------------------")
        print("🔐 ------------------------ Azure Integration ----------------------")
        print("-------------------------------------------------------------------")
        try:
            config = Config()

            azure_service = Azure(config=config)

            # origin_path = "dags/g1_azure_upload.txt" # Dynamic
            origin_path = f"{config.platform.storage_local}/tickets_win.parquet"
            target_path = "test/tickets_win.parquet" # Fixed
            azure_service.upload_to_adls(
                origin_path = origin_path,
                target_path = target_path
            )
        except Exception as ex:
            print("Error al intentar subir a Azure Blob Storage:", ex)
            log.error("Error al intentar subir a Azure Blob Storage:", ex)

    ssh_azure_upload()

dag = ssh_azure_upload_dag()