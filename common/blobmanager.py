import os
import io
from azure.storage.blob import BlobServiceClient


class BlobManager:
    def __init__(self, conn_string, store_name):
        self.constring = conn_string
        self.storeName = store_name
        self.bsc = BlobServiceClient.from_connection_string(self.constring)

    def write_blob(self, file):
        blob_container_client = self.bsc.get_container_client(self.storeName)
        blob_client = blob_container_client.get_blob_client(file.filename)
        blob_client.upload_blob(file, blob_type="BlockBlob", overwrite=True)

    def read_blob(self, name):
        client = self.bsc.get_blob_client(container=self.storeName, blob=name)
        data = client.download_blob()
        return io.BytesIO(data.readall())
