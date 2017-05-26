
import mysql.connector
from mysql.connector import errorcode
import logging

class base_dao(object):
    config = {
      'user': 'root',
      'password': 'root',
      'host': '127.0.0.1',
      'database': 'backbone',
      'raise_on_warnings': True,
    }

    def __init__ (self):
        self._logger =  logging.getLogger()

    def get_connection(self):
        try:
          cnx = mysql.connector.connect(**self.config)
        except mysql.connector.Error as err:
          if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            self._logger.critical("Something is wrong with your user name or password")
          elif err.errno == errorcode.ER_BAD_DB_ERROR:
            self._logger.critical("Database does not exist")
          else:
            self._logger.critical(err)
        return cnx

