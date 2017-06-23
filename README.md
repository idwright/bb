To enable WSGI for Apache2 on Ubuntu do the following:

    apt install python3-pip
    pip3 install --upgrade pip
    pip3 install mod_wsgi

    mod_wsgi-express module-config | grep Load > /etc/apache2/mods-available/wsgi.load
    mod_wsgi-express module-config | grep -v Load > /etc/apache2/mods-available/wsgi.conf
    a2enmod wsgi

See server/overlay/bb-server.wsgi for specific configuration details
