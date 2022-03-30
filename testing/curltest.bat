curl -F "customerId=dfce4c80-ccd7-4a1a-a526-a7daf0e41541" \
     -F "fileType=gating" \
     -F "fileId=d0fef03b-0838-4326-934d-bc68c2316a83" \
     -F "file=@./DataSample.xlsx" \
     "http://localhost:7071/api/xldata"
