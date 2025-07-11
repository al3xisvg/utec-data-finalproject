from airflow.decorators import dag, task
from airflow.providers.microsoft.azure.hooks.wasb import WasbHook
from datetime import datetime, timedelta
import logging, time

from config.app import Config

log = logging.getLogger('airflow.task')

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

@dag(
    dag_id="azure_upload_basic_dag",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["azure", "blob", "upload"],
)
def upload_dag():

    @task
    def upload_file_to_blob():
        print("-------------------------------------------------------------------")
        print("🔐 ------------------------ Azure Integration ----------------------")
        print("-------------------------------------------------------------------")
        try:
            # Connect using the connection created in UI
            hook = WasbHook(wasb_conn_id="azure_blob_storage")

            config = Config()
            
            # Local file path (this must exist in your container or volume)
            # local_file_path = "/opt/airflow/data/sample.txt"
            local_file_path = f"{config.platform.storage_local}/tickets_win.parquet"
            
            # Container name in your blob storage
            container_name = "datalake"
            
            # The name the blob will have in Azure
            # blob_name = "datalake/raw/airflow/G01/tickets_win.parquet"
            blob_name = "raw/airflow/G01/tickets_win.parquet"

            # Upload the file
            hook.load_file(
                file_path=local_file_path,
                container_name=container_name,
                blob_name=blob_name,
                overwrite=True
            )

            print(f"Uploaded {local_file_path} to {container_name}/{blob_name}")
        except Exception as ex:
            print("Error al inventar subir a Blob Storage:", ex)
            log.error("Error al inventar subir a Blob Storage:", ex)

    upload_file_to_blob()

dag = upload_dag()
