import logging
import os

from common.BlobManager import BlobManager
from common.ServiceBusManager import ServiceBusManager
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:

    # load our form input parameters into variabless
    file = req.files.get('file')
    fileId = req.form.get('fileId')
    customerId = req.form.get('customerId')
    fileType = req.form.get('fileType')

    # create instances of our helper classes
    bm = BlobManager(
        os.environ["BlobStorageConnectionString"], os.environ["BlobStorageStoreName"])
    sbm = ServiceBusManager(
        os.environ["ServiceBusConnectionString"], os.environ["ServiceBusQueueName"])

    try:
        # write our file to blob storage
        bm.write_blob(file)

        # create a message and enqueue it in our service bus
        message = {}
        message["id"] = fileId
        message["name"] = file.filename
        message["customerId"] = customerId
        message["type"] = fileType
        sbm.enqueue(message)

        # respond to the caller
        return func.HttpResponse(f"{file.filename} was uploaded successfully.")
    except Exception as ex:
        logging.info(ex)
        return func.HttpResponse(ex.message)
