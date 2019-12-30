
from functools import total_ordering

@total_ordering
class vertex:
	def __init__(self, id, weight = 1, partition = -1, gain = 0):
		self.id = id
		self.weight = weight
		# when we collapse verteces we keep track of the old verteces
		self.collapsed_verteces = []
		
		# shortcut
		# indices go hand in hand:
		# e.g.: self and connected_verteces[2] are connected by connected_edges[2]
		self.connected_verteces = []
		self.connected_edges = []

		# partition stuff
		self.partition = partition
		self.locked = False
		self.gain = 0

	# compare id's
	def __eq__(self, other):
		return self.id == other.id

	def to_string(self):
		print("vertex: id: ", self.id, " weight: ", self.weight)

	def __lt__(self, other):
		return self.gain < other.gain