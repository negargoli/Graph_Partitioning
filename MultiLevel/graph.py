
import edge
import vertex

class graph:
	def __init__(self, edges, verteces):
		self.edges = edges
		self.verteces = verteces
		self.max_vertex_id = len(verteces)
		self.max_edge_id = len(edges)

		# these are the edges that are collapsed
		# they are part of the maximal matching
		self.removed_edges = []

		# partition partial lists
		self.unlocked_verteces = []
		self.locked_verteces = []


	def collapse_verteces(self, vertex_0_id, vertex_1_id):
		# get a new id for the new vertex
		new_vertex_id = self.max_vertex_id
		self.max_vertex_id = self.max_vertex_id + 1

		# get the verteces from the id's
		vertex_0 = self.search_vertex_by_id(vertex_0_id)
		vertex_1 = self.search_vertex_by_id(vertex_1_id)

		# now remove the verteces since we will collapse them into a new vertex
		self.verteces.remove(vertex_0)
		self.verteces.remove(vertex_1)

		# create new vertex from the old verteces:
		new_vertex = vertex.vertex(new_vertex_id, vertex_0.weight + vertex_1.weight)
		new_vertex.collapsed_verteces.append(vertex_0);
		new_vertex.collapsed_verteces.append(vertex_1);
		self.verteces.append(new_vertex)

		# purge all the edges that are adjascent to the deleted verteces:	
		for index, cur_edge in enumerate(self.edges):
			if cur_edge.node_0 is vertex_0_id or cur_edge.node_0 is vertex_1_id:
				cur_edge.node_0 = new_vertex_id
			if cur_edge.node_1 is vertex_0_id or cur_edge.node_1 is vertex_1_id: 
				cur_edge.node_1 = new_vertex_id

		# check for duplicate edges and collapse them
		seen = []
		
		for cur_edge in self.edges:
			if cur_edge not in seen:
				seen.append(cur_edge)
			else:
				# collapse the edge!
				seen[seen.index(cur_edge)].weight += cur_edge.weight 
				seen[seen.index(cur_edge)].collapsed_edges.append(cur_edge)
				# remove it from the graph
				self.edges.remove(cur_edge)

		self.edges = seen;


	def search_vertex_by_id(self, find_me):
		graph_verteces = self.verteces
		for cur_vertex in graph_verteces:
			if find_me is cur_vertex.id:
				return cur_vertex

		# error! Did not find the requested vertex
		assert(1 == 0)

	def to_string(self):
		# debugging
		print("Graph edges: ")
		for cur_edge in self.edges:
			cur_edge.to_string()

		print("Graph verteces: ")
		for cur_vertex in self.verteces:
			cur_vertex.to_string()

	def to_string_verbose(self):
		# debugging
		print("Graph edges: ")
		for cur_edge in self.edges:
			cur_edge.to_string()
			if cur_edge.collapsed_edges:
				print("child edges: ")
				for child_edge in cur_edge.collapsed_edges:
					child_edge.to_string()
				print("child edges over")

		print("Graph verteces: ")
		for cur_vertex in self.verteces:
			cur_vertex.to_string()
			if cur_vertex.collapsed_verteces:
				print("child verteces: ")
				for child_vertex in cur_vertex.collapsed_verteces:
					child_vertex.to_string()
				print("child verteces over ")

	# shortcut for faster lookup
	def vertex_X_vertex(self):
		for cur_vertex in self.verteces:
			for cur_edge in self.edges:
				if cur_edge.node_0 is cur_vertex.id:
					cur_vertex.connected_verteces.append(self.search_vertex_by_id(cur_edge.node_1))
					cur_vertex.connected_edges.append(cur_edge)
					assert(cur_edge.node_0 is not cur_edge.node_1)
				elif cur_edge.node_1 is cur_vertex.id:
					cur_vertex.connected_verteces.append(self.search_vertex_by_id(cur_edge.node_0))
					cur_vertex.connected_edges.append(cur_edge)
					assert(cur_edge.node_0 is not cur_edge.node_1)

	def compute_graph_cost(self):
		cost = 0
		for cur_edge in self.edges:
			vertex_0 = self.search_vertex_by_id(cur_edge.node_0)
			vertex_1 = self.search_vertex_by_id(cur_edge.node_1)

			if vertex_0.partition is not vertex_1.partition:
				cost += cur_edge.weight

	def compute_all_gains(self):
		for cur_vertex in self.unlocked_verteces:
			# reset the gain:
			cur_vertex.gain = 0

			# compute the new gain
			for index, other_vertex in enumerate(cur_vertex.connected_verteces):
				if cur_vertex.partition is other_vertex.partition:
					cur_vertex.gain -= cur_vertex.connected_edges[index].weight
				else:
					cur_vertex.gain += cur_vertex.connected_edges[index].weight 

		self.unlocked_verteces.sort(reverse=True) 

	def print_stats(self):
		print("Graph stats:")
		print("Number of edges: ", len(self.edges))
		print("Number of verteces: ", len(self.verteces))