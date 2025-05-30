from airflow.decorators import dag, task
from pendulum import datetime, timezone
import logging, time

from services.ssh import SSHService
from services.odoo import OdooService

from config.app import Config

log = logging.getLogger('airflow.task')

@dag(
    dag_id="ssh_tunnel_dag",
    description="DAG para conectarse por ssh a una base de datos Odoo",
    start_date=datetime(2025, 1, 1, tz=timezone("America/Lima")),
    schedule=None,
    catchup=False,
    tags=["config"],
)
def ssh_tunnel_dag():

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
            df_tickets_win = odoo_service.direct_consult("tickets_win")
            print("---df_tickets_win---")
            print(df_tickets_win.head())
        except Exception as ex:
            print("Error al establecer la conexión SSH o a la base de datos:", ex)
            log.error("Error al establecer la conexión SSH o a la base de datos:", ex)
        finally:
            ssh_service.close()

    ssh_tunnel()

dag = ssh_tunnel_dag()
