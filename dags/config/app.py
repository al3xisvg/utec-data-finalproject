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

class AzureConfig:
    def __init__(self, tenant_id: str, client_id: str, client_secret: str, storage_account_name: str, container_name: str):
        self.tenant_id      = tenant_id
        self.client_id      = client_id
        self.client_secret  = client_secret
        self.account_url    = f"https://{storage_account_name}.blob.core.windows.net"
        self.container_name = container_name

class OdooConfig:
    def __init__(self, remote: DBHostConfig, local: DBHostConfig, name: Optional[str], user: Optional[str], pwd: Optional[str]):
        self.remote = remote
        self.local  = local
        self.name   = name
        self.user   = user
        self.pwd    = pwd

class MongoDBConfig:
    def __init__(self, srv: str):
        self.srv = srv

class Platform:
    def __init__(self, storage_local: str):
        self.storage_local = storage_local

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

        self.mongodb=MongoDBConfig(
            srv         = os.getenv('MONGODB_SRV')
        )

        self.azure = AzureConfig(
            tenant_id               = os.getenv('AZURE_TENANT_ID'),
            client_id               = os.getenv('AZURE_CLIENT_ID'),
            client_secret           = os.getenv('AZURE_CLIENT_SECRET'),
            storage_account_name    = os.getenv('AZURE_STORAGE_ACCOUNT_NAME'),
            container_name          = os.getenv('AZURE_CONTAINER_NAME')
        )

        self.platform = Platform(
            storage_local   = os.getenv('STORAGE_LOCAL')
        )