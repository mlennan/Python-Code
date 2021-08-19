from tkinter import *
from tkinter import ttk
from os import listdir
from os import scandir
from os import path
from os import getcwd
from os import walk
from os import chdir
from os import remove
from os import rmdir
from shutil import move

selected = None
all_text_widgets = []
move_target = None


#thewidget.cget("text")    gets the text displayed by a label

def get_directory_contents():
	all_directories = get_path_directories()
	all_directories = sorted(all_directories, key=str.casefold)
	all_files = get_files()
	all_files = sorted(all_files, key=str.casefold)
	return all_directories + all_files

def get_path_directories():
	all_directories = ["..."]
	for root, dirs, files in walk("."):
		for directory in dirs:
			all_directories.append(directory)
		return all_directories


def get_files():
	all_files = []
	for root, dirs, files in walk("."):
		for everyfile in files:
			all_files.append(everyfile)
		return all_files

def text_widget_creation_process(all_entries):
	global all_text_widgets
	for text_widget in all_text_widgets:
		text_widget.destroy()
	global selected
	selected = None
	all_text_widgets = []
	current_column = 1
	current_row = 1
	# all_entries = get_directory_contents()
	for entry in all_entries:
		label = label_creation(entry)
		all_text_widgets.append(label)
		label.grid(column = current_column, row = current_row)
		current_column = current_column + 1
		if current_column > 5:
			current_column = 1
			current_row = current_row + 1
	

# Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
# first5columns_width = sum([buttons[0][j].winfo_width() for j in range(0, 5)])
# first5rows_height = sum([buttons[i][0].winfo_height() for i in range(0, 5)])
# frame_canvas.config(width=first5columns_width + vsb.winfo_width(),
#                     height=first5rows_height)


def label_creation(filename):
	label = ttk.Label(label_frame, text=filename, padding="10 10 10 10")
	label.configure(wraplength = 200)
	label.bind('<Enter>', lambda f: label.configure(foreground="blue"))
	label.bind('<Leave>', lambda f: check_if_selected(label))#l.configure(foreground="black"))
	label.bind('<1>', lambda f: set_selected(label))#lambda e: l.configure(text='Clicked left mouse button'))
	label.bind('<Double-1>', lambda f: double_click())
	# l.bind('<B3-Motion>', lambda f: l.configure(text='right button drag to %d,%d' % (e.x, e.y)))
	return label



def check_if_selected(widget_target):
	if widget_target != selected:
		widget_target.configure(foreground ="black")

def set_selected(widget_target):
	global selected
	if selected != None and selected != widget_target:
		selected.configure(foreground="black")		#can't get past this after changing folders
	selected = widget_target

def double_click():
	destination = None
	if selected.cget("text") == "...":			#can't get past this after changing folders
		destination = getcwd()[0:(getcwd().rfind("/"))]
	else:
		destination = getcwd() + "/" + selected.cget("text")
	try:
		chdir(destination)
		text_widget_creation_process(get_directory_contents())	
	except OSError:
		print("Did not change directory")
#		open_file()
		pass


def delete_file():
	# if selected.cget("text") != "...":
	if path.exists(selected.cget("text")):
		try:
			remove(selected.cget("text"))
			text_widget_creation_process(get_directory_contents())
		except OSError:
			try:
				rmdir(selected.cget("text"))
				text_widget_creation_process(get_directory_contents())
			except OSError:
				print("Directory is not empty")
			except Error as error_caught:
				print(f"Could not delete, {error_caught}")

	else:
		print("Selected item not deletable")

def set_move():
	global move_target
	move_target = getcwd() + "/" + selected.cget("text")

def execute_move():
	global move_target
	if move_target == None:
		okay_window = Toplevel()
		okay_window.columnconfigure(0, weight=1)
		okay_window.rowconfigure(0, weight=1)
		okay_frame = ttk.Frame(okay_window, padding ="15 15 15 15")
		okay_frame.grid(column=0, row=0, sticky=(N, W, E, S))
		okay_button = ttk.Button(okay_frame, text = 'Okay', command = lambda: okay_window.destroy())
		okay_button.grid(column=2, row=3)
		ttk.Label(okay_frame, text="Select a file to move first").grid(column=2, row=2)
	else:
		try:
			move(move_target, getcwd())
			text_widget_creation_process(get_directory_contents())
		except Error as error_caught:
			print("Failed to move file, " + error_caught)


def execute_search(search_text):
	all_results = []
	print("Starting search")
	for root, directs, files in walk("."):
		for directory in directs:
			for file in files:
				if search_text in file:
					all_results.append(file)
			print(f"Now searching in {directory}")
			if search_text in directory:
				all_results.append(directory)
	print("Search complete")
	text_widget_creation_process(all_results)




root = Tk()
root.title("File Manager")
label_frame = ttk.Frame(root, padding="60 60 120 120")
label_frame.grid(column=1, row=1, sticky=(N, W, E, S))
# canvas_containter = ttk.Frame(root, padding = "5 5 5 5")
# canvas_containter.grid(column=10, row=10, sticky=(N, W, E, S))
# label_canvas = Canvas(label_frame)
# label_canvas.grid(column = 0, row = 0)
button_frame = ttk.Frame(root, padding = "5 5 5 5")
button_frame.grid(column=0, row=1, sticky=(N, W, E, S))
top_frame = ttk.Frame(root, padding = "5 5 5 5")
top_frame.grid(column = 1, row = 0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# label_frame.grid_propagate(False)
# scrollbar = Scrollbar(label_frame)
# scrollbar.grid(column = 999, row = 0, sticky = (N, S))
text_widget_creation_process(get_directory_contents())

delete_button = ttk.Button(button_frame, text = 'Delete', command = lambda: delete_file())
root.bind('<Control-d>', lambda f: delete_file())
delete_button.grid(column = 0, row = 0)
move_button = ttk.Button(button_frame, text = 'Set Move', command = lambda: set_move())
move_button.grid(column = 0, row = 1)
execute_move_button = ttk.Button(button_frame, text = 'Execute Move', command = lambda: execute_move())
execute_move_button.grid(column = 0, row = 2)

search_entry = StringVar()
search_bar = ttk.Entry(top_frame, textvariable = search_entry)
search_bar.grid(column = 3, row = 0)
search_button = ttk.Button(top_frame, text = 'Search', command = lambda: execute_search(search_entry.get()))
search_button.grid(column = 4, row = 0)
finish_button = ttk.Button(top_frame, text = 'Finish Search', command = lambda: text_widget_creation_process(get_directory_contents()))
finish_button.grid(column = 5, row = 0)

root.mainloop()









