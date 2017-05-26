
import mysql.connector
from mysql.connector import errorcode

config = {
  'user': 'root',
  'password': 'root',
  'host': '127.0.0.1',
  'database': 'backbone',
  'raise_on_warnings': True,
}

try:
  cnx = mysql.connector.connect(**config)
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
	cursor = cnx.cursor()

	query = ("SELECT id from entities")

#	hire_start = datetime.date(1999, 1, 1)
#	hire_end = datetime.date(1999, 12, 31)

#	cursor.execute(query, (hire_start, hire_end))

#	for (first_name, last_name, hire_date) in cursor:
#	  print("{}, {} was hired on {:%d %b %Y}".format(
#		last_name, first_name, hire_date))

	cursor.close()
	cnx.close()
