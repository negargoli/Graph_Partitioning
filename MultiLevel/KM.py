
import sys
import partition
import utility

def compute_all_gains_KM(unlocked_cells, list_of_nets):
	# first, set all gains to 0:
	for uc in unlocked_cells:
		uc.gain = 0

	# now update the gains
	# traverse each net
	for net in list_of_nets:

		# error checking
		assert(len(net.stakeholder_cells)>1)

		# for each cell in the net, detect whether it is the only cell
		# in a given partition
		for cell in net.stakeholder_cells:

			# early exit condition
			if not cell in unlocked_cells:
				break;

			# get the partition of the current cell
			my_partition = cell.partition
			# assume I am the only cell with my_partition
			only_one = True
			all_of_us = True

			# traverse all other cells
			for other_cell in net.stakeholder_cells:
				if other_cell is not cell and other_cell in unlocked_cells:
					if other_cell.partition is my_partition:
						only_one = False
					else:
						assert(other_cell.partition is not my_partition)
						all_of_us = False

			#if only_one:
				#assert(not all_of_us)
			#if all_of_us:
				#assert(not only_one)

			# if only_one holds, then update the gain
			if only_one:
				for uc in unlocked_cells:
					if uc is cell:
						uc.gain += 1
			if all_of_us:
				for uc in unlocked_cells:
					if uc is cell:
						uc.gain -= 1

		return unlocked_cells

# check if cell is the only cell in a given partition
def is_only_cell(cell, list_of_cells):
	my_partition = cell.partition
	for other in list_of_cells:
		if cell.id is other.id:
			continue
		else:
			if other.partition is my_partition:
				return False
	return True

# check if net is complete
# if all cells in a list have the same partition, the net is complete!
def is_net_complete(list_of_cells):
	my_partition = list_of_cells[0].partition 
	for cur_cell in list_of_cells:
		if cur_cell.partition is not my_partition:
			return False
	return True

# KM gain computation
def gain_compute(unlocked_cells, list_of_nets, fudge_factor = 1):

	# first, set all gains to 0:
	for uc in unlocked_cells:
		uc.gain = 0

	# for each cell in all unlocked cells
	for cell in unlocked_cells:

		# traverse all the nets
		for net in list_of_nets:
			if cell in net.stakeholder_cells:
				# check if net is complete
				if is_net_complete(net.stakeholder_cells):
					# decrement the gain, we would ruin a complete net!
					cell.gain -= 1 * fudge_factor
				# chkec is net is off by 1 cell
				if is_only_cell(cell, net.stakeholder_cells):
					# increment the gain because we would complete a net!
					cell.gain += 1 * fudge_factor

	# return the updated list, all the gains ahve been updated
	return unlocked_cells


def kernigan_lin_KM(list_of_cells, list_of_nets):

	pass_count = 6
	min_cost = sys.maxsize
	
	for cur_pass in range(0, pass_count):
		
		# unlock all cells
		unlocked_cells = list_of_cells[:]
		
		# randomly assign partitions
		unlocked_cells = partition.permute_partition(unlocked_cells)
		initial_pass_cost = partition.compute_total_cost(list_of_nets, unlocked_cells)
		#print("iteration: ", cur_pass, " pre_KL_cost: ", initial_pass_cost) 
		
		# debugging:
		# utility.print_list_helper(unlocked_cells)

		# error checking
		assert(unlocked_cells)

		# locked cells, empty inititally
		locked_cells = []

		[p0_count, p1_count] = partition.verify_partition_count(unlocked_cells)

		# define the cur_partition
		# cur partition decides which partition to swap an element from
		cur_partition = None
		if p0_count > p1_count:
			cur_partition = 0
		else:
			cur_partition = 1

		while unlocked_cells:
			# compute all the gains of the unlocked cells
			#unlocked_cells = compute_all_gains(unlocked_cells)

			# compute all gains, based on the KM algorithm
			unlocked_cells = gain_compute(unlocked_cells, list_of_nets)

			# get the max gain cells
			max_cells = sorted(unlocked_cells, reverse=True)

			# pick a valid move
			for i in range(len(max_cells)):
				if max_cells[i].partition is cur_partition:
					break;

			# swap the partitions
			max_cells[i].partition = (max_cells[i].partition + 1) % 2
			cur_partition = (cur_partition + 1) % 2

			# add cell to locked list 
			assert(max_cells[i] not in locked_cells)
			locked_cells.append(max_cells[i])
			unlocked_cells.remove(max_cells[i])

			# verification
			partition.verify_partition_count(locked_cells)

			#
			# debugging information
			#
			# print("locked_cells")
			# utility.print_list_helper(locked_cells)
			# print("unlocked_cells")
			# utility.print_list_helper(unlocked_cells)

			# get current cost
			final_pass_cost = partition.compute_total_cost(list_of_nets, locked_cells + unlocked_cells) 
			min_cost = min(final_pass_cost, min_cost)

		# all iterations of the pass have terminated, final pass verdict:
		#print("iteration: ", cur_pass, " final_pass cost: ", final_pass_cost, " overall min_cost: ", min_cost)

	# return the min_cost
	return min_cost