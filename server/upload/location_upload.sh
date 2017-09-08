SPLIT_SIZE=1000



for SOURCE in manage_sites_samples manage_sites pv_3_locations
do
    split -l ${SPLIT_SIZE} ${SOURCE}.txt ${SOURCE}_split_

    SKIP='?skipHeader=true'
    for i in ${SOURCE}_split_*
    do
        echo ${i}
        UPDATE_ONLY='&updateOnly=true'
        if [ ${SOURCE} = 'manage_sites_samples' ]
        then
            ENT_TYPE=
        else
            ENT_TYPE='&entityType=location'
        fi

        time curl --header 'Content-Type: multipart/form-data' --header 'Accept: application/json' -F additionalMetadata="@${SOURCE}.json;type=text/json" -F dataFile="@${i};type=text/csv" "http://localhost:8080/v1/source/${SOURCE}/upload${SKIP}${UPDATE_ONLY}${ENT_TYPE}"
        SKIP='?skipHeader=false'
        if [ $? -eq 0 ]
        then
            rm ${i}
        fi
    done
done

curl --header 'Content-Type: multipart/form-data' --header 'Accept: application/json' -F additionalMetadata="@location_pf_6.json;type=text/json" -F dataFile="@pf_6_metadata.txt;type=text/csv" 'http://localhost:8080/v1/source/location_pf_6/upload?skipHeader=true&entityType=location'

for SOURCE in spotmalaria vobs genre vivax
do
    curl --header 'Content-Type: multipart/form-data' --header 'Accept: application/json' -F additionalMetadata="@roma_location.json;type=text/json" -F dataFile="@${SOURCE}.txt;type=text/csv" "http://localhost:8080/v1/source/location_${SOURCE}/upload?skipHeader=true&entityType=location"
done
