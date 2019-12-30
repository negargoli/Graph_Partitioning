
from functools import total_ordering

@total_ordering
class edge:
	def __init__(self, node_0, node_1, weight=1):
		self.node_0 = node_0
		self.node_1 = node_1
		self.weight = weight

		# when we collapse edges we keep track of the old edges
		self.collapsed_edges = []

	def __eq__(self, other):
		return ((self.node_0 is other.node_0) and (self.node_1 is other.node_1)
			or (self.node_1 is other.node_0) and (self.node_0 is other.node_1))

	def __lt__(self, other):
		return self.weight < other.weight

	def to_string(self):
		print("edge: node_0: ", self.node_0, \
			" node_1: ", self.node_1, \
			" weight: ", self.weight)