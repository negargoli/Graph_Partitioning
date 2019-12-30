
from functools import total_ordering

# block class
@total_ordering
class block:
	def __init__(self, id):
		self.id = id 
		self.grid_location = [] 
		self.root_net = []
		self.stakeholder_cells = []
		self.gain = -1

	def assign_location(self, grid_location):
		self.grid_location = grid_location

	def dist(self, other):
		return abs(self.grid_location[0] - other.grid_location[0]) + abs(self.grid_location[1] - other.grid_location[1])

	def __eq__(self, other):
		return (self.id == other.id)

	def __lt__(self, other):
		return self.gain < other.gain
