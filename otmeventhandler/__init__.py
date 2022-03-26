import json
import openpyxl
import logging

from common.BlobManager import BlobManager
import azure.functions as func

# since this is a service bus triggered function, we get our 
# queue message here as an argument to our main method
def main(msg: func.ServiceBusMessage):
    # decode and convert response into a python dict
    qmsg = msg.get_body().decode('utf-8')
    msg = json.loads(qmsg)

    # create an instance of our blob manager and extract the
    # blob that matches the file name that we got from our 
    # service bus message
    bm = BlobManager()
    bytes = bm.read_blob(msg['name'])

    # locate the handler that corresponds to the type that we got
    # from our service bus message and process the contents of the file
    try:
        class_name = f"{msg['type'].capitalize()}Processor"
        module = __import__(f"common.{class_name}", fromlist=[''])
        class_ = getattr(module, class_name)
        handler = class_()
        handler.process(xldocument=openpyxl.load_workbook(bytes))
    except Exception as ex:
        # need to do more here to ensure that we are aware of failures.
        logging.error(ex)
