BUILD=0
VIRTUAL_ENV_HOME=.
VIRTUAL_ENV_HOME=/home/iwright/git/bb-local
if [ ${BUILD} = 1 ]
then
    virtualenv server-env -p /usr/bin/python3
    unzip python-flask-server-generated.zip
    cp -pr python-flask-server bb-server
fi
source ${VIRTUAL_ENV_HOME}/server-env/bin/activate
pip3 install -r bb-server/requirements.txt
cd bb-server
export PYTHONPATH=$(pwd):${PYTHONPATH}
echo "http://localhost:8080/v1/ui/"
python3 -m swagger_server
