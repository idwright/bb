split -l 1000 oxford_central_samples.csv oxford_central_samples_split_

for i in oxford_central_samples_split_aa
do
curl --header 'Content-Type: multipart/form-data' --header 'Accept: application/json' -F additionalMetadata="@oxford_central_samples.json;type=text/json" -F dataFile="@${i};type=text/csv" 'http://localhost:8080/v1/source/oxford_central_samples/upload' 
done
rm oxford_central_samples_split_*
