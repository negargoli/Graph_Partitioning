
import block

# net class
class net:
	def __init__(self, root, num_connections):
		self.root = root 
		self.num_connections = num_connections
		self.connections = []
		self.grid_location = []

	def __eq__(self, other):
		return self.root is other.root
		
	def add_connection(self, connection_index):
		self.connections.append(connection_index)

	# cost function
	def compute_cost(self, list_of_cells):

		# get the root cell
		root_cell = serch_blocks_by_id(self.root, list_of_cells)

		# set the bounding box extrimities to the root cell's coords
		# this is a bounding box of one single point for now
		# the box will be expanded iteratively
		min_x = root_cell.grid_location[0]
		max_x = root_cell.grid_location[0]
		min_y = root_cell.grid_location[1]
		max_y = root_cell.grid_location[1]

		# debugging information
		# print(root_cell.id, root_cell.grid_location)

		# compare every connection net against the current bounding box
		for cur_elem in self.connections:
			connected_cell = serch_blocks_by_id(cur_elem, list_of_cells)
			min_x = min(min_x, connected_cell.grid_location[0])
			max_x = max(max_x, connected_cell.grid_location[0])
			min_y = min(min_y, connected_cell.grid_location[1])
			max_y = max(max_y, connected_cell.grid_location[1])

			# print(connected_cell.id, connected_cell.grid_location)

		# the bounding has been maximized now
		# error checking
		assert(max_x >= min_x)
		assert(max_y >= min_y)

		# print(min_x, max_x, min_y, max_y)

		# return the cost, the half perimeter of the bounding box:
		return max_x - min_x + max_y - min_y

	def get_src_location(self, cell_list):
		root_cell = serch_blocks_by_id(self.root, cell_list)
		return root_cell.grid_location

	def get_dst_locations(self, cell_list):
		dst_locations = []

		for cell_index in self.connections:
			dst_cell = serch_blocks_by_id(cell_index, cell_list)
			dst_locations.append(dst_cell.grid_location)

		return dst_locations