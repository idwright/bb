
import logging
import mysql.connector
from mysql.connector import errorcode
import psycopg2
from psycopg2.extras import register_uuid
from psycopg2.extras import LoggingConnection

import logging.config

logging.config.fileConfig('../backbone_server/dao/logging.conf')

class BaseDAO(object):
    config = {
        'user': 'root',
        'password': 'root',
        'host': '127.0.0.1',
        'database': 'backbone',
        'raise_on_warnings': True,
    }

    psql_config = {
        'user': 'iwright',
        'database': 'backbone'
    }

    _postgres = False

    _db_true = 1
    _db_false = 0

    _connection = None
    _cursor = None

    def __init__(self):
        #logging.basicConfig(level=logging.DEBUG)
        self._logger = logging.getLogger(__name__)
        #logging.getLogger('connexion.apis.flask_api').setLevel(logging.DEBUG)
        if self._postgres:
            psycopg2.extensions.register_type(register_uuid())
            psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
            psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
            self._db_true = 't'
            self._db_false = 'f'

    def get_connection(self):
        if self._postgres:
            conn = psycopg2.connect(connection_factory=LoggingConnection, **self.psql_config )
            conn.initialize(self._logger)
            cur = conn.cursor()
            cur.execute("SET search_path TO " + 'backbone,public')
            cur.close()
        else:
            try:
                conn = mysql.connector.connect(**self.config)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    self._logger.critical("Something is wrong with your user name or password")
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    self._logger.critical("Database does not exist")
                else:
                    self._logger.critical(err)
        return conn

    @staticmethod
    def insert_statement(stmt):
        if BaseDAO._postgres:
            return stmt + ' RETURNING id'
        else:
            return stmt

    @staticmethod
    def inserted_id(cursor):
        if BaseDAO._postgres:
            return(cursor.fetchone()[0])
        else:
            return(cursor.lastrowid)

    @staticmethod
    def _decode(value):
        if BaseDAO._postgres:
            return value
        else:
            return value.decode('utf-8')
