import mysql.connector
from mysql.connector import Error



def create_connection(host_name, user_name, user_password):
	connection = None
	try:
		connection = mysql.connector.connect(
			host=host_name,
			user=user_name,
			passwd=user_password,
			port=3306
		)
		print("Connection to MySQL DB successful")
	except Error as e:
		print(f"The error '{e}' occurred")

	return connection


def create_connection_db_named(host_name, user_name, user_password, db_name):
	connection_db_named = None
	try:
		connection_db_named = mysql.connector.connect(
			host=host_name,
			user=user_name,
			passwd=user_password,
			database = db_name
		)
		print("Connection to named MySQL DB successful")
	except Error as e:
		print(f"The error '{e}' occurred, did not connect to named database")

	return connection_db_named



def create_database(connection, query):
	cursor = connection.cursor()
	try:
		cursor.execute(query)
		print("Database created successfully")
	except Error as e:
		print(f"The error '{e}' occurred")


def execute_query(connection, query):
	cursor = connection.cursor()
	try:
		cursor.execute(query)
		connection.commit()
		print("Query successfully executed")
	except Error as e:
		print(f"The error '{e}' has occured")


username = input('Insert username')
password = input('Insert password')
ip = input('Insert IP')
connection = create_connection(ip, username, password)

create_database_query = "CREATE DATABASE sm_app"
create_database(connection, create_database_query)

connection = create_connection_db_named(ip, username, password, "sm_app")

create_users_table = """
CREATE TABLE IF NOT EXISTS users2 (id INT AUTO_INCREMENT, name TEXT NOT NULL, age INT, gender TEXT, nationality TEXT, PRIMARY KEY (id)) ENGINE = InnoDB
"""

execute_query(connection, create_users_table)
