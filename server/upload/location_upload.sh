SPLIT_SIZE=1000



for SOURCE in manage_sites manage_sites_samples pv_3_sanger_source_code_metadata pv_3_locations
do
    split -l ${SPLIT_SIZE} ${SOURCE}.txt ${SOURCE}_split_

    SKIP='?skipHeader=true'
    for i in ${SOURCE}_split_*
    do
        echo ${i}
        if [ ${SOURCE} = 'sanger_ega_dataset' ]
        then
            UPDATE_ONLY='&updateOnly=true'
        else
            UPDATE_ONLY=
        fi
        if [ ${SOURCE} = 'pv_3_sanger_source_code_metadata_XXXXXXXX' ]
        then
            ENT_TYPE='&entityType=sample'
        else
            ENT_TYPE=
        fi
        time curl --header 'Content-Type: multipart/form-data' --header 'Accept: application/json' -F additionalMetadata="@${SOURCE}.json;type=text/json" -F dataFile="@${i};type=text/csv" "http://localhost:8080/v1/source/${SOURCE}/upload${SKIP}${UPDATE_ONLY}${ENT_TYPE}"
        SKIP='?skipHeader=false'
        if [ $? -eq 0 ]
        then
            rm ${i}
        fi
    done
done

