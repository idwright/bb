SPLIT_SIZE=1000

if [ "$1" = 'all' ]
then
    SOURCE=oxford_central_donor_parent
    split -l ${SPLIT_SIZE} virtual_donor_parent_mother_table_oxford_02JUN2017.csv ${SOURCE}_split_
SKIP=true

    for i in ${SOURCE}_split_*
    do
        time curl --header 'Content-Type: multipart/form-data' --header 'Accept: application/json' -F additionalMetadata="@oxford_central_samples.json;type=text/json" -F dataFile="@${i};type=text/csv" "http://localhost:8080/v1/source/${SOURCE}/upload?skipHeader=${SKIP}"
    SKIP=false
        if [ $? -eq 0 ]
        then
            rm ${i}
        fi
    done

    SOURCE=oxford_central_donor
    split -l ${SPLIT_SIZE} virtual_sample_donor_table_oxford_02JUN2017.csv ${SOURCE}_split_
SKIP=true

    for i in ${SOURCE}_split_*
    do
        time curl --header 'Content-Type: multipart/form-data' --header 'Accept: application/json' -F additionalMetadata="@oxford_central_donor.json;type=text/json" -F dataFile="@${i};type=text/csv" "http://localhost:8080/v1/source/${SOURCE}/upload?skipHeader=${SKIP}"
    SKIP=false
        if [ $? -eq 0 ]
        then
            rm ${i}
        fi
    done
fi

SOURCE=oxford_central_samples
split -l ${SPLIT_SIZE} legacy_samples_table_oxford_02JUN2017.csv ${SOURCE}_split_
SKIP=true
for i in ${SOURCE}_split_*
do
    time curl --header 'Content-Type: multipart/form-data' --header 'Accept: application/json' -F additionalMetadata="@oxford_central_samples.json;type=text/json" -F dataFile="@${i};type=text/csv" "http://localhost:8080/v1/source/${SOURCE}/upload?skipHeader=${SKIP}"
    SKIP=false
    if [ $? -eq 0 ]
    then
        rm ${i}
    fi
done


