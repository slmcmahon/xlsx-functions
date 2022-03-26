import logging

from common.blobmanager import BlobManager
from common.servicebusmanager import ServiceBusManager
import azure.functions as func


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