import json
import openpyxl
import logging
import os

from opencensus.ext.azure.log_exporter import AzureLogHandler
from common.BlobManager import BlobManager
import azure.functions as func

logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(
    connection_string=os.environ["AppInsightsKey"]))
# since this is a service bus triggered function, we get our
# queue message here as an argument to our main method


def main(msg: func.ServiceBusMessage):
    # decode and convert response into a python dict
    qmsg = msg.get_body().decode('utf-8')
    msg = json.loads(qmsg)
    file_name = msg['name']

    # create an instance of our blob manager and extract the
    # blob that matches the file name that we got from our
    # service bus message
    bm = BlobManager()
    bytes = bm.read_blob(file_name)

    # locate the handler that corresponds to the type that we got
    # from our service bus message and process the contents of the file
    try:
        # ensure that the incoming type is capitalized to match the name of the class
        # in common.processors
        class_name = msg['type'].capitalize()
        module = __import__(f"common.processors.{class_name}", fromlist=[''])

        # dynamically load the class and pass in the workbook from blobstorage
        class_ = getattr(module, class_name)
        handler = class_(openpyxl.load_workbook(bytes))

        if handler.validate():
            handler.process()
            logger.info(f"Processing {file_name} for type {class_name}.")
        else:
            logger.error(
                f"Could not validate input for {class_name}.  File: {file_name}.")

    except Exception as ex:
        # need to do more here to ensure that we are aware of failures.
        logging.error(ex)
