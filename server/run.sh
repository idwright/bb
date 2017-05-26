BUILD=1
VIRTUAL_ENV_HOME=.
if [ ${BUILD} = 1 ]
then
    virtualenv server-env -p /usr/bin/python3
    (cd ..;./generate.sh)
fi
if [ -f ${VIRTUAL_ENV_HOME}/server-env/bin/activate ]
then
    source ${VIRTUAL_ENV_HOME}/server-env/bin/activate
    pip3 install -r bb-server/requirements.txt
    pip3 install -r backbone_server/REQUIREMENTS
    cp -pr overlay/* bb-server
    export PYTHONPATH=$(pwd):$(pwd)/bb-server:${PYTHONPATH}
    cd bb-server
    echo "http://localhost:8080/v1/ui/"
    python3 -m swagger_server
fi
