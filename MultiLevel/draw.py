# library imports
from graphics import *
import random
import time

# my imports
import utility
import partition

def clear(win):
    for item in win.items[:]:
        item.undraw()
    win.update()
    return win

def setup_window(win, window_width, window_height):
	win = GraphWin('Layout', 1024, 1024)
	win.setCoords(0.0, 0.0, window_width, window_height)
	win.setBackground("white")
	return win

def color_square(win, x, y, color):
	square = Rectangle(Point(x,y), Point(x+1,y+1))
	square.draw(win)
	square.setFill(color)
	return win

def number_square(win, x, y, number):
	label = Text(Point(x+0.5, y+0.5), number)
	label.draw(win)
	return win

def draw_grid(win, window_width, window_height):
# draw grid
	for x in range(window_height):
		line = Line(Point(0, x), Point(window_width, x))
		line.draw(win)    
	for x in range(window_width):
		line = Line(Point(x, 0), Point(x, window_height))
		line.draw(win)
	return win

def number_cells(win, list_of_cells):
	for cur_cell in list_of_cells:
		grid_location = cur_cell.grid_grid_location
		number_square(win, grid_location[0], grid_location[1], cur_cell.id)
	return win

def draw_connections(win, list_of_nets, list_of_cells):
	for cur_net in list_of_nets:
		src_grid_location = cur_net.get_src_grid_location(list_of_cells)
		src_x = src_grid_location[0]
		src_y = src_grid_location[1]
		dst_grid_locations = cur_net.get_dst_grid_locations(list_of_cells)

		for dst_grid_location in dst_grid_locations:
			dst_x = dst_grid_location[0]
			dst_y = dst_grid_location[1]
			line = Line(Point(src_x+0.48, src_y+0.48), Point(dst_x+0.48, dst_y+0.48))		
			line.draw(win)

	return win

def update_board(win, num_cols, num_rows, list_of_cells, list_of_nets):
	# clear the board
	win = clear(win)
	# draw the grid
	win = draw_grid(win, num_cols, num_rows)
	# draw the cells
	win = number_cells(win, list_of_cells)
	# draw the connections
	win = draw_connections(win, list_of_nets, list_of_cells)

	return win

def draw_full_board(win, num_cols, num_rows, list_of_cells, list_of_nets):
	# flush the board! - we are re-drawing from scratch
	win = setup_window(win, num_cols, num_rows)
	# draw the grid
	win = draw_grid(win, num_cols, num_rows)
	# draw the cells
	win = number_cells(win, list_of_cells)
	# draw the connections
	win = draw_connections(win, list_of_nets, list_of_cells)

	return win

def draw_net(win, net, list_of_cells, num_cols, num_rows):
	root_cell = utility.serch_blocks_by_id(net.root, list_of_cells)
	assert(root_cell)
	root_partition = root_cell.partition

	if not root_cell.grid_location:
		# assign a grid_location to the cell
		root_cell = utility.assign_random_partition_location_to_cell(root_cell, num_cols, num_rows)


	for cell_id in net.connections:

		# find the cell
		cell = utility.serch_blocks_by_id(cell_id, list_of_cells)
		assert(cell)

		# if the cell has no locaiton yet, assign one based on partition
		if not cell.grid_location:
			# assign a grid_location to the cell
			cell = utility.assign_random_partition_location_to_cell(cell, num_cols, num_rows)

		# draw the line
		line = Line(Point(root_cell.grid_location[0], root_cell.grid_location[1]), Point(cell.grid_location[0], cell.grid_location[1]))
		line.draw(win)

	return win

def draw_nets(win, num_cols, num_rows, list_of_nets, list_of_cells):
	for cur_net in list_of_nets:
		draw_net(win, cur_net, list_of_cells, num_cols, num_rows)
		# print("cost of net: ", partition.compute_cost(cur_net, list_of_cells))
		# win.getMouse()
	return win

def partition_board(win, num_cols, num_rows):
	square = Rectangle(Point(0,0), Point(int(num_cols/2),num_rows))
	square.draw(win)
	square.setFill('red')
	square = Rectangle(Point(num_cols,num_rows), Point(int(num_cols/2),0))
	square.draw(win)
	square.setFill('green')
	return win

def draw_cells(win, list_of_cells):
	for cell in list_of_cells:
		label = Text(Point(cell.grid_location[0], cell.grid_location[1]), cell.id)
		label.draw(win)
	return win

def draw_final_result(win, num_cols, num_rows, list_of_cells, list_of_nets):
	win = setup_window(win, num_cols, num_rows)

	win = partition_board(win, num_cols, num_rows)

	win = draw_nets(win, num_cols, num_rows, list_of_nets, list_of_cells)

	win = draw_cells(win, list_of_cells)
	
	return win