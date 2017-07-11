test -f swagger-codegen-cli.jar || wget http://central.maven.org/maven2/io/swagger/swagger-codegen-cli/2.2.2/swagger-codegen-cli-2.2.2.jar -O swagger-codegen-cli.jar
rm -rf python-flask-server
java -jar swagger-codegen-cli.jar generate -i swagger.yaml -l python-flask -o python-flask-server
rm -rf server/bb-server
cp -pr python-flask-server server/bb-server
java -jar swagger-codegen-cli.jar generate -i swagger.yaml -l typescript-angular2 -o typescript-angular2-client -c client.config.json
sed -i -e 's/models\.Array/Array/' typescript-angular2-client/model/Entities.ts typescript-angular2-client/model/Summary.ts
for i in threshold sources include
do
sed -i -e "s/${i} instanceof Date/${i}/" -e "s/${i}.d.toISOString()/${i}/" typescript-angular2-client/api/ReportApi.ts
done
for i in start count orderby
do
sed -i -e "s/${i} instanceof Date/${i}/" -e "s/${i}.d.toISOString()/${i}/" typescript-angular2-client/api/EntityApi.ts
done
for i in skipHeader updateOnly start count orderby
do
sed -i -e "s/${i} instanceof Date/${i}/" -e "s/${i}.d.toISOString()/${i}/" typescript-angular2-client/api/SourceApi.ts
done
java -jar swagger-codegen-cli.jar generate -i swagger.yaml -l python -o python_client -c client.config.json
