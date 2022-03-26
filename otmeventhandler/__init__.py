import json
import openpyxl

from common.blobmanager import BlobManager
import azure.functions as func


def main(msg: func.ServiceBusMessage):
    # decode and convert response into a python dict
    qmsg = msg.get_body().decode('utf-8')
    msg = json.loads(qmsg)

    bm = BlobManager()
    bytes = bm.read_blob(msg['name'])

    handler = __import__(f"common.{msg['type']}handler", fromlist=[''])
    handler.process(openpyxl.load_workbook(bytes))
