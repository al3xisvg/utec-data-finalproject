from azure.identity import ClientSecretCredential
from azure.storage.blob import BlobServiceClient

import logging

from config.app import Config

log = logging.getLogger('airflow.task')

class Azure:
    def __init__(self, config: Config):
        self.container_name = config.azure.container_name

        # Azure AD - Login
        self.credential = ClientSecretCredential(
            tenant_id = config.azure.tenant_id,
            client_id = config.azure.client_id,
            client_secret = config.azure.client_secret
        )

        # Storage Account - Cnx
        self.blob_service_client = BlobServiceClient(
            account_url = config.azure.account_url,
            credential = self.credential
        )

    def upload_to_adls(self, origin_path: str, target_path: str):
        blob_client = self.blob_service_client.get_blob_client(
            container = self.container_name,
            blob = target_path
        )

        with open(origin_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
