from dotenv import load_dotenv
from typing import Optional
import os

class SSHConfig:
    def __init__(self, host: Optional[str], user: Optional[str], private_key: Optional[str]):
        self.host = host
        self.user = user
        self.private_key = private_key

class DBHostConfig:
    def __init__(self, host: Optional[str], port: int):
        self.host = host
        self.port = port

class OdooConfig:
    def __init__(self, remote: DBHostConfig, local: DBHostConfig, name: Optional[str], user: Optional[str], pwd: Optional[str]):
        self.remote = remote
        self.local  = local
        self.name   = name
        self.user   = user
        self.pwd    = pwd

class Config:
    def __init__(self):
        load_dotenv()

        self.ssh = SSHConfig(
            host        =   os.getenv('SSH_HOST'),
            user        =   os.getenv('SSH_USER'),
            private_key =   os.getenv('SSH_PRIVATE_KEY_PATH')
        )

        self.odoo = OdooConfig(
            remote=DBHostConfig(
                host    =   os.getenv('DB_REMOTE_HOST'),
                port    =   int(os.getenv('DB_REMOTE_PORT', 5432))
            ),
            local=DBHostConfig(
                host    =   os.getenv('DB_LOCAL_HOST'),
                port    =   int(os.getenv('DB_LOCAL_PORT', 5432))
            ),
            name        =   os.getenv('DB_NAME'),
            user        =   os.getenv('DB_USER'),
            pwd         =   os.getenv('DB_PASSWORD')
        )