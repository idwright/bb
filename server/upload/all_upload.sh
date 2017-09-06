SPLIT_SIZE=1000


./oxford_central_samples_upload.sh

for SOURCE in vobs genre spotmalaria vivax vw_vrpipe pf_6_metadata pv_3_sanger_source_code_metadata pv_3_broad_metadata pv_3_broad_sra_accessions pv_3_chapellhill_sra_accessions
    #sanger_ega_dataset 
do
    split -l ${SPLIT_SIZE} ${SOURCE}.txt ${SOURCE}_split_

    SKIP='?skipHeader=true'
    for i in ${SOURCE}_split_*
    do
        echo ${i}
        if [ ${SOURCE} = 'vobs' -o ${SOURCE} = 'genre' -o ${SOURCE} = 'spotmalaria' -o ${SOURCE} = 'vivax' ]
        then
            ENT_TYPE='&entityType=sample'
            UPDATE_ONLY=
        else
            ENT_TYPE=
            UPDATE_ONLY='&updateOnly=true'
        fi
        time curl --header 'Content-Type: multipart/form-data' --header 'Accept: application/json' -F additionalMetadata="@${SOURCE}.json;type=text/json" -F dataFile="@${i};type=text/csv" "http://localhost:8080/v1/source/${SOURCE}/upload${SKIP}${UPDATE_ONLY}${ENT_TYPE}"
        SKIP='?skipHeader=false'
        if [ $? -eq 0 ]
        then
            rm ${i}
        fi
    done
done

./location_upload.sh
