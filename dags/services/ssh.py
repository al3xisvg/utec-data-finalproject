from sshtunnel import SSHTunnelForwarder
import psycopg2

from config.app import Config

class SSHService:
    def __init__(self, config: Config):
        self.ssh_host = config.ssh.host
        self.ssh_user = config.ssh.user
        self.ssh_private_key_path = config.ssh.private_key
        self.db_remote_host = config.odoo.remote.host
        self.db_remote_port = config.odoo.remote.port
        self.db_local_host = config.odoo.local.host
        self.db_local_port = config.odoo.local.port
        self.db_name = config.odoo.name
        self.db_user = config.odoo.user
        self.db_password = config.odoo.pwd
        self.tunnel = None
        self.connection = None

    def start_ssh_tunnel(self):
        self.tunnel = SSHTunnelForwarder(
            (self.ssh_host, 22),
            ssh_username=self.ssh_user,
            ssh_pkey=self.ssh_private_key_path,
            remote_bind_address=(self.db_remote_host, self.db_remote_port),
            local_bind_address=(self.db_local_host, self.db_local_port),
            set_keepalive=60
        )
        self.tunnel.start()
        print(f"Túnel SSH establecido en {self.db_local_host}:{self.tunnel.local_bind_port}")

    def connect_to_db(self):
        if not self.tunnel.is_active:
            self.start_ssh_tunnel()

        self.connection = psycopg2.connect(
            dbname=self.db_name,
            user=self.db_user,
            password=self.db_password,
            host=self.db_local_host,
            port=self.tunnel.local_bind_port,
            connect_timeout=60,
            options="-c statement_timeout=120000"
        )
        print("Conexión a la base de datos establecida.")

    def execute_query(self, query):
        if not self.connection:
            raise Exception("No hay conexión a la base de datos.")
        
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            return result

    def close(self):
        if self.connection:
            self.connection.close()
            print("Conexión a la base de datos cerrada.")
        if self.tunnel:
            self.tunnel.stop()
            print("Túnel SSH cerrado.")
