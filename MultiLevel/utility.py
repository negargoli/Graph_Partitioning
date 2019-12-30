import block
import net

import random

def serch_blocks_by_id(find_me, all_cells):
	for cur_cell in all_cells:
		if cur_cell.id == find_me:
			return cur_cell

	# this is only reached when a block is connected to but 
	# in itself doesn't have any connections
	return []

def add_net_as_stakeholder(cell, net, list_of_cells):
	# add net root
	if net.root is not cell.id:
		cur_connection_cell = serch_blocks_by_id(net.root, list_of_cells)
		if cur_connection_cell not in cell.stakeholder_cells:
			cell.stakeholder_cells.append(cur_connection_cell)

	# add net connections
	for cur_connection in net.connections:
		if cur_connection is not cell.id:
			cur_connection_cell = serch_blocks_by_id(cur_connection, list_of_cells)
			if cur_connection_cell not in cell.stakeholder_cells:
				cell.stakeholder_cells.append(cur_connection_cell)

def block_X_block(list_of_cells, list_of_nets):
	for cur_cell in list_of_cells:
		for cur_net in list_of_nets:
			# check if the root of the net is the current cell
			if cur_net.root is cur_cell.id or cur_cell.id in cur_net.connections:
				add_net_as_stakeholder(cur_cell, cur_net, list_of_cells)
	return list_of_cells

def create_cells(num_cells, num_cols, num_rows, list_of_nets):

	# keep a list of all the placed cells
	list_of_cells = [] # no cells have been placed yet

	# create all blocks that initiate connections
	for i in list_of_nets:
		# i will serve as the if for the instantiated cells
		cell = block.block(i.root)
		if cell not in list_of_cells:
			list_of_cells.append(cell)

	# create all outstanding blocks
	for cur_net in list_of_nets:
		for net_connect in cur_net.connections:
			if not serch_blocks_by_id(net_connect, list_of_cells):
				# this block hasn't been created yet, create it
				cell = block.block(net_connect)
				list_of_cells.append(cell)

	return list_of_cells

def assign_random_partition_location_to_cell(cell, num_cols, num_rows):
	random_y = random.uniform(0, num_rows)
	if cell.partition:
		random_x = random.uniform(0, int(num_cols/2))
	else:
		random_x = random.uniform(int(num_cols/2), num_cols)

	cell.grid_location = [random_x, random_y]
	return cell

def print_list_helper(list_of_cells):
	print("printing list of cells:")
	for cell in list_of_cells:
		print("id: ", cell.id, " partition: ", cell.partition, " gain: ", cell.gain)
	print("done printing list")

def get_stakeholder_cells_for_net(list_of_nets, list_of_cells):
	# for each net:
	for cur_net in list_of_nets:
		# all the cells linked to this net
		stakeholder_cells = []

		# get the root cell
		root_cell = serch_blocks_by_id(cur_net.root, list_of_cells)
		assert(root_cell)
		stakeholder_cells.append(root_cell)

		# get the connected cells
		for cur_connection in cur_net.connections:
			connected_cell = serch_blocks_by_id(cur_connection, list_of_cells)
			assert(connected_cell)
			if connected_cell not in stakeholder_cells:
				stakeholder_cells.append(connected_cell)

		cur_net.stakeholder_cells = stakeholder_cells

	return list_of_nets