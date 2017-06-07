test -f swagger-codegen-cli.jar || wget http://central.maven.org/maven2/io/swagger/swagger-codegen-cli/2.2.2/swagger-codegen-cli-2.2.2.jar -O swagger-codegen-cli.jar
rm -rf python-flask-server
java -jar swagger-codegen-cli.jar generate -i swagger.yaml -l python-flask -o python-flask-server
rm -rf server/bb-server
cp -pr python-flask-server server/bb-server
java -jar swagger-codegen-cli.jar generate -i swagger.yaml -l typescript-angular2 -o typescript-angular2-client -c client.config.json
sed -i -e 's/models\.Array/Array/' typescript-angular2-client/model/Entities.ts typescript-angular2-client/model/Summary.ts
sed -i -e 's/threshold instanceof Date/threshold < 0/' -e 's/threshold.d.toISOString()/threshold/' typescript-angular2-client/api/ReportApi.ts
