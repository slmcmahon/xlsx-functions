$uri = "http://localhost:7071/api/xldata"

$form = @{
    file = Get-Item -Path ./DataSample.xlsx
    customerId = "dfce4c80-ccd7-4a1a-a526-a7daf0e41541"
    fileType = "gating"
    fileId = "d0fef03b-0838-4326-934d-bc68c2316a83"
}

Invoke-RestMethod -Method POST -Uri $uri -Form $form
