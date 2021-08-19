def initialize_sudoku():	#TODO: get input from user
	initial_sudoku = [
[3, 0, 7,   0, 1, 0,   0, 2, 0],
[0, 4, 0,   0, 0, 3,   0, 0, 0],
[5, 0, 1,   2, 0, 0,   0, 4, 0],

[0, 8, 0,   0, 0, 0,   3, 0, 6],
[0, 0, 0,   0, 5, 0,   0, 0, 0],
[0, 0, 0,   0, 0, 9,   0, 5, 0],

[1, 0, 3,   9, 8, 0,   0, 0, 0],
[0, 2, 0,   0, 7, 0,   0, 0, 0],
[0, 0, 0,   0, 0, 0,   0, 8, 0]
]
	return initial_sudoku



def check_viability(current_attempted_number, attempted_x, attempted_y, current_board):
	if not check_across_viability(current_attempted_number, attempted_y, current_board):
		return False
	if not check_down_viability(current_attempted_number, attempted_x, current_board):
		return False
	return check_box_viability(current_attempted_number, attempted_x, attempted_y, current_board)

def check_across_viability(current_attempted_number, attempted_x, current_board):
	for current_column in range(9):
		if current_board[attempted_x][current_column] == current_attempted_number:	#if the number we're trying to place in the box has already been used it's not viable
			return False
	return True

def check_down_viability(current_attempted_number, attempted_y, current_board):
	for current_row in range(9):
		if current_board[current_row][attempted_y] == current_attempted_number:	#if the number we're trying to place in the box has already been used it's not viable
			return False
	return True

def check_box_viability(current_attempted_number, attempted_x, attempted_y, current_board):
	sudoku_box_x = attempted_x//3	#0-2 = first, 3-5 = second, 6-8 = third column
	sudoku_box_y = attempted_y//3	#same as above but for rows
	for box_index_x in range(3):
		for box_index_y in range(3):
			if current_board[box_index_y + (3*sudoku_box_y)][box_index_x + (3*sudoku_box_x)] == current_attempted_number:	#if the number we're trying to place in the box has already been used it's not viable
				return False
	return True

def interpret_attempted_position(attempted_x, attempted_y):	#manually determines what each number should return 
	if attempted_x < 3:	#boxes are 0,1,2
		if attempted_y < 3:
			return 0
		if attempted_y < 6:
			return 1
		return 2

	if attempted_x < 6:	#boxes are 3,4,5
		if attempted_y < 3:
			return 3
		if attempted_y < 6:
			return 4
		return 5

	if attempted_y < 3:	#boxes are 6,7,8
		return 6
	if attempted_y < 6:
		return 7
	return 8

def interpret_attempted_position_v2(attempted_x, attempted_y):	#each if doesn't need three return statements so we can condense the code
	increment
	if attempted_y < 3:
		increment = 0
	elif attempted_y < 6:
		increment = 1
	else:
		increment = 2

	if attempted_x < 3:
		return increment
	if attempted_x < 6:
		return increment + 3
	return increment + 6

def interpret_attempted_position_v3(attempted_x, attempted_y):	# what was essentially done to attempted_y can also be done to attempted_x
	return attempted_y//3 + attempted_x//3						# this is just moved into the method that used to call it

def find_empty_index(current_board):
	for current_row in range(9):
		for current_column in range(9):
			if current_board[current_row][current_column] == 0:
				return (current_row, current_column)

def solve_sudoku(current_board):
	empty_coordinates = find_empty_index(current_board)
	if empty_coordinates == None:	#if there aren't any more boxes to fill in
		return current_board
	current_y, current_x = empty_coordinates	#turn coordinate tuple into seperate coordinate variables
	for current_attempted_number in range(1,10):
		if check_viability(current_attempted_number, current_x, current_y, current_board):
			current_board[current_y][current_x] = current_attempted_number	#a number without a duplicate down, across, or in the same 3x3 box
			if solve_sudoku(current_board):
				return True
			current_board[current_y][current_x] = 0	#the number we put in the box didn't work so don't use it
	return False

def print_board(finished_board):	#prints the resulting board into its nine 3x3 squares, spacing them out from each other
	for current_row in range(9):
		sudoku_line = ""
		for current_column in range(9):
			sudoku_line += str(finished_board[current_row][current_column])
			if (current_column%3) == 2:
				sudoku_line+= " "
		print(sudoku_line)
		if (current_row%3) == 2:
			print("")


initial_board = initialize_sudoku()
solve_sudoku(initial_board)
print_board(initial_board)






