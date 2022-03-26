import logging

def process(xl):
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