import sys

base_dir='.'
server_dir=base_dir

#This is equivalent to the apache2 configuration below
#e.g. if running using 
#mod_wsgi-express start-server /var/www/html/backbone-server/bb-server/bb-server.wsgi 
# Note that the swagger server config still needs to match hostname, port etc
if False:
        base_dir='/var/www/html/backbone-server'
        server_dir=base_dir + '/bb-server'

        sys.path.append(base_dir)
        sys.path.append(server_dir)

        activate_this = base_dir + '/server-env/bin/activate_this.py'
        with open(activate_this) as file_:
            exec(file_.read(), dict(__file__=activate_this))

#                WSGIDaemonProcess backbone processes=2 threads=25 python-path=/var/www/html/backbone-server python-home=/var/www/html/backbone-server/server-env home=/var/www/html/backbone-server/bb-server
#                WSGIProcessGroup backbone
#                WSGIScriptAlias /v1 /var/www/html/backbone-server/bb-server/bb-server.wsgi
#
#		<Directory "/var/www/html/backbone-server/bb-server">
#			<Files bb-server.wsgi>
#			    Require all granted
#			</Files>
#			Options FollowSymLinks
#			AllowOverride None
#			Order deny,allow
#			Allow from all
#			#Authtype CAS
#			#CASAuthNHeader On
#
#			#require valid-user
#			#require cas-attribute memberOf:cn=wg,ou=sims,ou=projects,ou=groups,dc=malariagen,dc=net
#
#		</Directory>

import connexion
from swagger_server.encoder import JSONEncoder


app= connexion.App(__name__, specification_dir=server_dir+'/swagger_server/swagger/')
app.app.json_encoder = JSONEncoder
app.add_api('swagger.yaml', arguments={'title': 'No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)'})


class PathRewriteMiddleware:

    def __init__(self, application):
        self.__application = application

    def __call__(self, environ, start_response):

#This is for when WSGIScriptAlias is something other than /
#Otherwise swagger will return a 404 json response
        if not environ['PATH_INFO'].startswith(environ['SCRIPT_NAME']):
                environ['PATH_INFO'] = environ['SCRIPT_NAME'] + environ['PATH_INFO']
                environ['SCRIPT_NAME'] = ''

        def _start_response(status, headers, *args):
            return start_response(status, headers, *args)

        return self.__application(environ, _start_response)

application = PathRewriteMiddleware(app)