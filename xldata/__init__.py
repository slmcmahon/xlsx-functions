import logging
import json
import os

from common.blobmanager import BlobManager
import azure.functions as func
from azure.servicebus import ServiceBusClient, ServiceBusMessage

from common.servicebusmanager import ServiceBusManager

SERVICE_BUS_CONNECTION_STRING = os.environ["ServiceBusConnectionString"]
SERVICE_BUS_QUEUE_NAME = os.environ["ServiceBusQueueName"]


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    file = req.files.get('file')
    fileId = req.form.get('fileId')
    customerId = req.form.get('customerId')
    fileType = req.form.get('fileType')

    bm = BlobManager()
    sbm = ServiceBusManager()

    try:
        bm.write_blob(file)
        
        message = {}
        message["id"] = fileId
        message["name"] = file.filename 
        message["customerId"] = customerId
        message["type"] = fileType
        sbm.enqueue(message)
        
        return func.HttpResponse(f"{file.filename} was uploaded successfully.")
    except Exception as ex:
        logging.info(ex)
        return func.HttpResponse(ex)