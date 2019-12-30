import graph
import edge
import vertex

import random


def assign_initial_partition(G):

	verteces = G.verteces
	random.shuffle(verteces)

	i = 0
	for cur_vertex in verteces:
		cur_vertex.partition = i % 2
		i = i + 1

def verify_parition_count(G):
	count_0 = 0
	count_1 = 0

	for vertex in G.verteces:
		if vertex.partition == 0:
			count_0 += 1
		else:
			assert(vertex.partition == 1)
			count_1 += 1

	count_delta = abs(count_0 - count_1)
	assert(count_delta <= 1)

def partition_graph(G):

	assign_initial_partition(G)
	verify_parition_count(G)

	# reset the verteces
	G.locked_verteces = []
	G.unlocked_verteces = G.verteces

	# start swapping
	while(G.unlocked_verteces):

		# compute all gains
		G.compute_all_gains()

		if len(G.unlocked_verteces + G.locked_verteces) % 2 == 0:
			# even swap
			assert(1==1)
		else:
			# uneven swap
			assert(1==1)





	return G
