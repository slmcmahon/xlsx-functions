import logging
import json
import os

import azure.functions as func
from azure.storage.blob import BlobServiceClient
from azure.servicebus import ServiceBusClient, ServiceBusMessage

SERVICE_BUS_CONNECTION_STRING = os.environ["ServiceBusConnectionString"]
SERVICE_BUS_QUEUE_NAME = os.environ["ServiceBusQueueName"]
BLOBSTORE_CONNECTION_STRING = os.environ["BlobStorageConnectionString"]
BLOBSTORE_STORE_NAME = os.environ["BlobStorageStoreName"]


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    file = req.files.get('file')
    fileId = req.form.get('fileId')
    customerId = req.form.get('customerId')
    fileType = req.form.get('fileType')

    try:
        store_file(file)
        enqueue_message(file.filename, fileId, customerId, fileType)
        return func.HttpResponse(f"{file.filename} was uploaded successfully.")
    except Exception as ex:
        logging.info(ex)
        return func.HttpResponse(ex)


def enqueue_message(fileName, fileId, customerId, fileType):
    message = {
        "id": f"{fileId}",
        "name": f"{fileName}",
        "customerId": f"{customerId}",
        "type": f"{fileType}"
    }
    sbmessage = ServiceBusMessage(json.dumps(message))
    servicebus_client = ServiceBusClient.from_connection_string(
        SERVICE_BUS_CONNECTION_STRING)
    with servicebus_client:
        sender = servicebus_client.get_queue_sender(
            queue_name=SERVICE_BUS_QUEUE_NAME)
        sender.send_messages([sbmessage])


def store_file(file):
    filename = file.filename
    blob_service_client = BlobServiceClient.from_connection_string(
        BLOBSTORE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(
        BLOBSTORE_STORE_NAME)
    blob_client = container_client.get_blob_client(filename)
    blob_client.upload_blob(file, blob_type="BlockBlob", overwrite=True)
