from airflow.decorators import dag, task
from pendulum import datetime, timezone
import logging, time

from services.ssh import SSHService
from services.odoo import OdooService
from services.mongodb import MongoDBService

from config.app import Config

log = logging.getLogger('airflow.task')

@dag(
    dag_id="extract_sources",
    description="DAG para conectarse por ssh a una base de datos Odoo",
    start_date=datetime(2025, 1, 1, tz=timezone("America/Lima")),
    schedule=None,
    catchup=False,
    tags=["config"],
)
def extract_sources():

    @task
    def ssh_tunnel():
        print("-------------------------------------------------------------------")
        print("🔐 -------------------------- SSH Config: --------------------------")
        print("-------------------------------------------------------------------")
        try:
            config = Config()
            ssh_service = SSHService(config=config)
            ssh_service.start_ssh_tunnel()
            time.sleep(3)
            ssh_service.connect_to_db()
            time.sleep(2)
            odoo_service = OdooService(ssh_service.connection)
            mongodb_service = MongoDBService(config=config)

            df_tickets_win = odoo_service.direct_consult("tickets_win")
            df_tickets_win.to_parquet(f"{config.platform.storage_local}/tickets_win.parquet", engine="pyarrow", index=False)

            df_accounts = mongodb_service.list_accounts()
            df_accounts.to_parquet(f"{config.platform.storage_local}/accounts.parquet", engine="pyarrow", index=False)
        
            df_requirements = mongodb_service.list_requirements()
            df_requirements.to_parquet(f"{config.platform.storage_local}/requirements.parquet", engine="pyarrow", index=False)
        except Exception as ex:
            print("Error al establecer la conexión SSH o a la base de datos:", ex)
            log.error("Error al establecer la conexión SSH o a la base de datos:", ex)
        finally:
            ssh_service.close()

    ssh_tunnel()

dag = extract_sources()
