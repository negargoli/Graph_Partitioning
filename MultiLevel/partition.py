import random
import sys
import math

import utility
import block
import KM

def assign_initial_partition(list_of_cells):
	i = 0
	for cur_cell in list_of_cells:
		cur_cell.partition = i % 2
		i = i + 1

	return list_of_cells

def verify_partition_count(list_of_cells):
	p0_count = 0
	p1_count = 0

	for cur_cell in list_of_cells:
		assert(cur_cell.partition is 0 or cur_cell.partition is 1)
		if cur_cell.partition is 0:
			p0_count = p0_count + 1 
		else:
			p1_count = p1_count + 1

	delta_count = abs(p0_count - p1_count)

	# this will cause an error if the partition is unbalanced
	assert( delta_count is 0 or delta_count is 1)

	# return the counts
	return[p0_count, p1_count]


# compute the gain function according to:
# Gain(v) = #incident edges that cross partition - #incident edges that do not
def compute_gain(cur_cell):
	number_of_edges = len(cur_cell.stakeholder_cells)

	# 2 count variables
	cross_partition_edges = 0
	within_partition_edges = 0

	for connected_node in cur_cell.stakeholder_cells:
		if connected_node.partition == cur_cell.partition:
			within_partition_edges += 1
		else:
			cross_partition_edges += 1

	# error checking
	assert(number_of_edges == cross_partition_edges + within_partition_edges)

	# return the gain:
	gain = cross_partition_edges - within_partition_edges
	cur_cell.gain = gain
	return gain

def compute_all_gains(list_of_cells, list_of_nets):
	for cur_cell in list_of_cells:
		cur_cell.gain = compute_gain(cur_cell)

	# experimental
	list_of_cells = KM.gain_compute(list_of_cells, list_of_nets, 0.2)

	return list_of_cells

def compute_cost(net, list_of_cells):
	# get the root cell
	root_cell = utility.serch_blocks_by_id(net.root, list_of_cells)
	assert(root_cell)

	# get the connected cells
	for cur_connection in net.connections:
		connected_cell = utility.serch_blocks_by_id(cur_connection, list_of_cells)
		if not connected_cell:
			assert(connected_cell)

		# cost of net is 1 iff cur_connection.partition is not root_cell.partition
		if root_cell.partition is not connected_cell.partition:
			return 1 

	# None of the connections crossed the partition, cost is 0
	return 0

def compute_total_cost(list_of_nets, list_of_cells):
	total_cost = 0
	for cur_net in list_of_nets:
		cost_net = compute_cost(cur_net, list_of_cells)
		# error checking
		assert(cost_net is 0 or cost_net is 1)
		total_cost += cost_net
	return total_cost

# return the sorted list based on gain
# the cell with the highest gain will go first in the list
def get_max_gain_cells(unlocked_cells):
	return unlocked_cells.sort(reverse=True) 

def permute_partition(list_of_cells):
	# randomly permute the partition of the cells
	random.shuffle(list_of_cells)

	# assign partitions to each element
	partition_count = len(list_of_cells)
	for i in range(0, int(partition_count/2)):
		list_of_cells[i].partition = 0
	for i in range(int(partition_count/2), len(list_of_cells)):
		list_of_cells[i].partition = 1

	# make sure the partition is valid
	verify_partition_count(list_of_cells)

	# return the partitioned list
	return list_of_cells

def is_allowed_swap(list_of_cells, swap_candidate):
	# make sure the list is balanced
	[p0_count, p1_count] = verify_partition_count(list_of_cells)

	if swap_candidate.partition is 0:
		p0_count -= 1
		p1_count += 1
	else:
		p1_count -= 1
		p0_count += 1

	# will this swap throw the partition off balance?
	delta = abs(p0_count - p1_count)
	is_allowed_swap = (delta < 2)

	# return the result of the comparision
	return is_allowed_swap

#
# Swaps one cell
# this is to be used when the total number of cells is uneven
#
def uneven_swap(list_of_cells, max_cells, unlocked_cells, locked_cells):
	# find the cell with the highest gain
	# that will not throw the partition off balance
	swap_me = None
	for i in range(len(max_cells)):
		
		# error checking
		assert(max_cells[i])
		
		# will this cell throw locked_cells off balance?
		if is_allowed_swap(list_of_cells, max_cells[i]):
			swap_me = max_cells[i]
			# No, it won't. We found a valid swap
			break;

	# error checking, did we swapped ourselves into a bad situation
	if not swap_me:
		# no more swaps are possible
		return [list_of_cells, unlocked_cells, locked_cells, True]

	# swap the cell:
	#if swap_me.gain > 0:
	swap_me.partition = (swap_me.partition+1)%2

	# swapped cells are no longer unlocked
	unlocked_cells.remove(swap_me)

	# lock the cells:
	locked_cells.append(swap_me)

	# verification
	verify_partition_count(list_of_cells)

	# return
	return [list_of_cells, unlocked_cells, locked_cells, False]

#
# Swaps two cells
# this is to be used when the total number of cells is even
#
def even_swap(list_of_cells, max_cells, unlocked_cells, locked_cells):
	# find the cell with the highest gain
	# that will not throw the partition off balance
	swap_me_0 = None
	swap_me_1 = None
	for i in range(len(max_cells)):
		
		# error checking
		assert(max_cells[i])
		
		if (max_cells[i].partition is 0 and not swap_me_0):
			swap_me_0 = max_cells[i]
		if (max_cells[i].partition is 1 and not swap_me_1):
			swap_me_1 = max_cells[i]
		if (swap_me_0 and swap_me_1):
			break;

	# error checking, did we swapped ourselves into a bad situation
	if not swap_me_0 or not swap_me_1:
		# no more swaps are possible
		return [list_of_cells, unlocked_cells, locked_cells, True]

	# swap the cells:
	swap_me_0.partition = (swap_me_0.partition+1)%2
	swap_me_1.partition = (swap_me_1.partition+1)%2

	# swapped cells are no longer unlocked
	unlocked_cells.remove(swap_me_0)
	unlocked_cells.remove(swap_me_1)

	# lock the cells:
	locked_cells.append(swap_me_0)
	locked_cells.append(swap_me_1)

	# verification
	verify_partition_count(list_of_cells)

	# return
	return [list_of_cells, unlocked_cells, locked_cells, False]

def kernigan_lin(list_of_cells, list_of_nets):

	pass_count = 6

	best_solution_thus_far = None
	best_min_cost = sys.maxsize
	
	for cur_pass in range(0, pass_count):
		# set the min cost for the pass
		pass_min_cost = sys.maxsize
		best_pass_solution = None

		# unlock all cells
		unlocked_cells = list_of_cells[:]
		
		# randomly assign partitions
		unlocked_cells = permute_partition(unlocked_cells)
		initial_pass_cost = compute_total_cost(list_of_nets, unlocked_cells)
		#print("iteration: ", cur_pass, " pre_KL_cost: ", initial_pass_cost) 
		
		# debugging:
		# utility.print_list_helper(unlocked_cells)

		# error checking
		assert(unlocked_cells)

		# locked cells, empty inititally
		locked_cells = []

		while unlocked_cells:
			# compute all the gains of the unlocked cells
			#unlocked_cells = compute_all_gains(unlocked_cells)

			# compute all gains, based on the KM algorithm
			unlocked_cells = compute_all_gains(unlocked_cells, list_of_nets)

			# get the max gain cells
			max_cells = sorted(unlocked_cells, reverse=True)
			# utility.print_list_helper(max_cells)

			assert(len(max_cells) == len(unlocked_cells))

			if len(list_of_cells) % 2 is 0:
				[list_of_cells, unlocked_cells, locked_cells, Done] = \
				even_swap(list_of_cells, max_cells, unlocked_cells, locked_cells)
			else:
				[list_of_cells, unlocked_cells, locked_cells, Done] = \
				uneven_swap(list_of_cells, max_cells, unlocked_cells, locked_cells)

			# error checking
			assert(len(unlocked_cells) + len(locked_cells) == len(list_of_cells))

			# no more swaps are bossible even though unlocked_cells is not empty
			if Done:
				assert(False)
				locked_cells.extend(unlocked_cells)
				break;

			# update the min_cost
			final_pass_cost = compute_total_cost(list_of_nets, locked_cells+unlocked_cells)

			# did we find a better solution than our best solution thus far?
			if final_pass_cost < pass_min_cost:
				pass_min_cost = final_pass_cost
				best_pass_solution = locked_cells+unlocked_cells
		
		assert(len(locked_cells) == len(list_of_cells))
		if not Done:
			assert(len(unlocked_cells) == 0)

		if pass_min_cost < best_min_cost:
				best_min_cost = pass_min_cost
				best_solution_thus_far = best_pass_solution

		# print("pass cost: ", pass_min_cost, " overall min_cost thus far: ", best_min_cost)

		# debugging
		# utility.print_list_helper(locked_cells)

		#for cell in list_of_cells:
			#print(cell.id, " ", cell.partition)
		# next pass starts now!

	# return the min_cost
	return [best_min_cost, best_solution_thus_far]


