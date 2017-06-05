SPLIT_SIZE=1000


./oxford_central_samples_upload.sh

for SOURCE in sanger_ega_dataset vw_vrpipe pf_6_metadata pv_3_sanger_source_code_metadata pv_3_broad_metadata pv_3_broad_sra_accessions pv_3_locations pv_3_chapellhill_sra_accessions pv_3_sanger_source_code_metadata_test VOBS
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

