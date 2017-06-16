#!/bin/bash
export PYTHONPATH=$(pwd)/../../python_client
if [ ! -d client-env ]
then
    virtualenv client-env -p /usr/bin/python3
    source client-env/bin/activate
    pip3 install -r ../../python_client/requirements.txt
fi
source client-env/bin/activate
python3 all_tests.py
#python3 -m unittest test_source.TestSource.test_load_source_entities
