import logging
import json
import os
import io

import openpyxl

import azure.functions as func
from azure.storage.blob import BlobServiceClient


BLOBSTORE_CONNECTION_STRING = os.environ["BlobStorageConnectionString"]
BLOBSTORE_STORE_NAME = os.environ["BlobStorageStoreName"]


def main(msg: func.ServiceBusMessage):
    # decode and convert response into a python dict
    qmsg = msg.get_body().decode('utf-8')
    msg = json.loads(qmsg)

    # Create a blob service client based on our connection string
    blob_service_client = BlobServiceClient.from_connection_string(
        BLOBSTORE_CONNECTION_STRING)
    # create a blob client for our blob store and the current filename
    # that is specified in the dequeued message
    client = blob_service_client.get_blob_client(
        container=BLOBSTORE_STORE_NAME, blob=msg['name'])

    # extract the data from the blob and convert it to a BytesIO
    data = client.download_blob()
    bytes = io.BytesIO(data.readall())

    # open the excel document from the BytesIO object
    # and select the active sheet
    xl = openpyxl.load_workbook(bytes)
    sheet = xl.active

    # for each row in the sheet, do something with the data
    for row in sheet.iter_rows(min_row=2):
        id = row[0].value
        locationId = row[1].value
        latitude = row[2].value
        longitude = row[3].value
        eventType = row[4].value
        logging.info(
            f"{id} / {locationId} / {latitude} / {longitude} / {eventType}")
