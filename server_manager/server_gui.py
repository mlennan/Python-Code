from tkinter import *
from tkinter import ttk
import mysql.connector
from mysql.connector import Error

# fix todo's
# fix injection vulnerabilities
# 
# 


server_connection = None
server_database_connection = None


def create_window(window_text):	#first of three functions used in basic windows that say success or say failure because (message)
	okay_window = Toplevel()
	okay_window.columnconfigure(0, weight=1)
	okay_window.rowconfigure(0, weight=1)
	okay_frame = ttk.Frame(okay_window, padding ="15 15 15 15")
	okay_frame.grid(column=0, row=0, sticky=(N, W, E, S))
	okay_button = ttk.Button(okay_frame, text = 'Okay', command = lambda: okay_window.destroy())
	okay_button.grid(column=2, row=3)
	ttk.Label(okay_frame, text=window_text).grid(column=2, row=2)

	return okay_window



def username_and_password():	#creates a window
	new_window = Toplevel()
	window_frame = ttk.Frame(new_window, padding="40 40 40 40")
	window_frame.grid(column=0, row=0, sticky = (N, W, E, S))
	new_window.columnconfigure(0, weight=1)
	new_window.rowconfigure(0, weight=1)

	ttk.Label(window_frame, text='Input username, password, and IP').grid(column=1,row=0)

	ttk.Label(window_frame, text='Username:').grid(column=0,row=1)
	username = StringVar()
	name_entry = ttk.Entry(window_frame, textvariable = username)
	name_entry.grid(column=1,row=1)

	ttk.Label(window_frame, text='Password:').grid(column=0,row=2)
	password = StringVar()
	password_entry = ttk.Entry(window_frame, textvariable = password, show = '*')
	password_entry.grid(column=1,row=2)

	ttk.Label(window_frame, text='IP Address:').grid(column=0,row=3)
	ipAddress = StringVar()
	ip_entry = ttk.Entry(window_frame, textvariable = ipAddress)
	ip_entry.grid(column=1,row=3)

	login_button = ttk.Button(window_frame, text = 'Log in', command = lambda: log_in(username, password, ipAddress))
	login_button.grid(column=0, row=5)

	cancel_button = ttk.Button(window_frame, text = 'Cancel', command = lambda: new_window.destroy())
	cancel_button.grid(column=2,row=5)
	new_window.mainloop()

def log_in(username, password, ipAddress):	#executes an action
	try:
		global server_connection
		server_connection = mysql.connector.connect(host = ipAddress.get(), user = username.get(), passwd = password.get())
		login_bool_window = create_window('Successfully connected!')
	except Error as error_caught:
		login_bool_window = create_window(f'Failed to connect, {error_caught}')


def create_database_window():	#creates a window
	# if server_connection == None:
	# 	connection_window = create_window('You must log in before you can create a database')
	# else:
		connection_window = Toplevel()
		connection_window_frame = ttk.Frame(connection_window, padding="40 40 40 40")
		connection_window_frame.grid(column=0, row=0, sticky = (N, W, E, S))
		connection_window.columnconfigure(0, weight=1)
		connection_window.rowconfigure(0, weight=1)

		ttk.Label(connection_window_frame, text='Database name:').grid(column=0,row=1)
		database_name = StringVar()
		database_input = ttk.Entry(connection_window_frame, textvariable = database_name)
		database_input.grid(column=1,row=1)

		ttk.Label(connection_window_frame, text='Input a name for the database').grid(column=1,row=0)
		create_button = ttk.Button(connection_window_frame, text = 'Create', command = lambda: initiate_database_creation(database_name))
		create_button.grid(column=1, row=3)
		cancel_button = ttk.Button(connection_window_frame, text = 'Cancel', command = lambda: connection_window.destroy())
		cancel_button.grid(column=2, row=3)

def initiate_database_creation(database_name):	#executes an action
	try:
		cursor = server_connection.cursor()
#		cursor.execute(f"CREATE DATABASE %(sanitized_name)s", {'sanitized_name':database_name.get()})
		cursor.execute(		#injection vulnerability
			"""CREATE TABLE IF NOT EXISTS {database_name} (
  id INT AUTO_INCREMENT, 
  name TEXT NOT NULL, 
  age INT, 
  gender TEXT, 
  nationality TEXT, 
  PRIMARY KEY (id)
) ENGINE = InnoDB
""")
		creation_bool_window = create_window('Successfully created database!')
	except Error as error_caught:
		creation_bool_window = create_window(f'Error creating database, {error_caught}')

		
def connect_to_database():	#creates a window
	new_window = Toplevel()
	window_frame = ttk.Frame(new_window, padding="40 40 40 40")
	window_frame.grid(column=0, row=0, sticky = (N, W, E, S))
	new_window.columnconfigure(0, weight=1)
	new_window.rowconfigure(0, weight=1)

	ttk.Label(window_frame, text='Input username, password, IP, and database name').grid(column=1,row=0)

	ttk.Label(window_frame, text='Username:').grid(column=0,row=1)
	username = StringVar()
	name_entry = ttk.Entry(window_frame, textvariable = username)
	name_entry.grid(column=1,row=1)

	ttk.Label(window_frame, text='Password:').grid(column=0,row=2)
	password = StringVar()
	password_entry = ttk.Entry(window_frame, textvariable = password, show = '*')
	password_entry.grid(column=1,row=2)

	ttk.Label(window_frame, text='IP Address:').grid(column=0,row=3)
	ipAddress = StringVar()
	ip_entry = ttk.Entry(window_frame, textvariable = ipAddress)
	ip_entry.grid(column=1,row=3)

	ttk.Label(window_frame, text='Database Name:').grid(column=0,row=4)
	database_name = StringVar()
	database_entry = ttk.Entry(window_frame, textvariable = database_name)
	database_entry.grid(column=1,row=4)

	login_button = ttk.Button(window_frame, text = 'Log in', command = lambda: access_database(username, password, ipAddress, database_name))
	login_button.grid(column=0, row=5)

	cancel_button = ttk.Button(window_frame, text = 'Cancel', command = lambda: new_window.destroy())
	cancel_button.grid(column=2,row=5)
	new_window.mainloop()

def access_database(username, password, ipAddress, database_name):	#executes an action
	try:
		global server_database_connection
		server_database_connection = mysql.connector.connect(host = ipAddress.get(), user = username.get(), passwd = password.get(), database = database_name.get())
		access_bool_window = create_window('Successfully connected to the database!')
	except Error as error_caught:
		access_bool_window = create_window(f'Could not connect to {database_name}, {error_caught}')



def view_data():	#creates a window
	new_window = Toplevel()
	window_frame = ttk.Frame(new_window, padding="40 40 40 40")
	window_frame.grid(column=0, row=0, sticky = (N, W, E, S))
	new_window.columnconfigure(0, weight=1)
	new_window.rowconfigure(0, weight=1)

	table_data = None

	ttk.Label(window_frame, text='Which table should data be retrieved from?').grid(column=0, row=0)
	target_table = StringVar()
	table_entry = ttk.Entry(window_frame, textvariable = target_table)
	table_entry.grid(column=1, row=1)
	ttk.Label(window_frame, text='Which field should data be retrieved from?').grid(column=0, row=2)
	table_field = StringVar()
	field_entry = ttk.Entry(window_frame, textvariable = table_field)
	field_entry.grid(column=1, row=3)

	select_button = ttk.Button(window_frame, text = 'Select', command = lambda: display_data(select_table_data(target_table, table_field)))
	select_button.grid(column=1, row=4)

#	join_button = ttk.Button(window_frame, text = 'Join',command = lambda table_data: get_database_data(target_table))
#	join_button.grid(column=0, row=4)

	update_button = ttk.Button(window_frame, text = 'Update',command = lambda: update_database_data(target_table, ))
	update_button.grid(column=0, row=5)

def display_data(table_data):
	new_window = Toplevel()
	window_frame = ttk.Frame(new_window, padding = "40 40 40 40")
	window_frame.grid(column=0, row=0, sticky = (N, W, E, S))
	new_window.columnconfigure(0, weight=1)
	new_window.rowconfigure(0, weight=1)
	current_user = 0
	for user in table_data:
		print(current_user)
		ttk.Label(window_frame, text=user).grid(column=0, row=current_user)
		current_user = current_user + 1


def update_database_data():	#executes an action
	cursor = server_database_connection.cursor()
	result = None
	# try:

def select_table_data(target_table, table_field):	#executes an action
	try:
#sanitization attempts
		# cursor.execute(f"CREATE DATABASE %(sanitized_name)s", {'sanitized_name':database_name.get()})
		# cursor = server_database_connection.cursor()
		# cursor.execute("""
		# 	SELECT
		# 		%s
		# 	FROM
		# 		%s
		# 	""", (table_field.get(), target_table.get()))#{'sanitized_field':table_field.get()},{'sanitized_table_name':target_table.get()})
		# result = cursor.fetchall()
		# print(f'data grabbed={result}')
		# return result


		select_action = f'SELECT {table_field.get()} FROM {target_table.get()}'	#injection vulnerable
		print(select_action)
		cursor = server_database_connection.cursor()
		cursor.execute(select_action)
		result = cursor.fetchall()
		print('still here')
		return result
	except Error as error_caught:
		print('Done goofed')
		pass





def finish_management(root):	#executes an action
	try:
		server_connection.close()
	except Exception:
		print('Server was not initally connected to')
	try:
		server_database_connection.close()
	except Exception:
		print('No database was connected to')
	root.destroy()

root = Tk()
main_frame = ttk.Frame(root, padding="30 30 120 120")
main_frame.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
ttk.Label(main_frame, text="This is a basic SQL database manager").grid(column=2, row=2)

login_button = ttk.Button(main_frame, text='Log in', command=lambda: username_and_password())
login_button.grid(column=1, row=4)
login_database_button = ttk.Button(main_frame, text='Log into database', command=lambda: connect_to_database())
login_database_button.grid(column=2, row=4)
if server_connection != None or server_database_connection != None:
	create_database_button = ttk.Button(main_frame, text='Create database', command=lambda: create_database_window())
	create_database_button.grid(column=3, row=4)
	select_table_data_button = ttk.Button(main_frame, text='Database actions', command = lambda: view_data())
	select_table_data_button.grid(column=4, row=4)

done_button = ttk.Button(main_frame, text='Finish and log out', command=lambda: finish_management(root))
done_button.grid(column=0, row=10)


root.mainloop()