if [ -f ~/Downloads/swagger.yaml ]
then
    mv ~/Downloads/swagger.yaml ..
fi
if [ -f ~/Downloads/python-flask-server-generated.zip ]
then
    mv ~/Downloads/python-flask-server-generated.zip .;rm -rf python-flask-server;unzip python-flask-server-generated.zip
fi
rm -rf bb-server/; cp -pr python-flask-server bb-server
sed -i 's/inline_response201/inline_response_201/' bb-server/swagger_server/models/entities.py bb-server/swagger_server/models/inline_response_201.py
cp -pr overlay/* bb-server
diff overlay/swagger_server/controllers/ python-flask-server/swagger_server/controllers/
