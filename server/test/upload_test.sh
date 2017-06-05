SPLIT_SIZE=1000



for SOURCE in combination_key
do
    split -l ${SPLIT_SIZE} ${SOURCE}.txt ${SOURCE}_split_

    for i in ${SOURCE}_split_*
    do
        time curl --header 'Content-Type: multipart/form-data' --header 'Accept: application/json' -F additionalMetadata="@${SOURCE}.json;type=text/json" -F dataFile="@${i};type=text/csv" "http://localhost:8080/v1/source/${SOURCE}/upload"
        if [ $? -eq 0 ]
        then
            rm ${i}
        fi
    done
done

