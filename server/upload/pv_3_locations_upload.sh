curl --header 'Content-Type: multipart/form-data' --header 'Accept: application/json' -F additionalMetadata="@pv_3_locations.json;type=text/json" -F dataFile="@pv_3_locations.txt;type=text/csv" 'http://localhost:8080/v1/source/pv_3_locations/upload' 
