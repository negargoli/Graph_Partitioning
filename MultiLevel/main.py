
# library imports
# from graphics import *
import argparse

# my imports
import parser
import draw
import partition
import block
import utility
import KM
import coarsening
import graph
import coarse_partition

def main(file_name):
		
	# graphics 
	win = 0

	# parse the file
	parsed_result = parser.parse_file(file_name)
	num_cells = parsed_result[0]
	num_connections = parsed_result[1]
	num_rows = parsed_result[2]
	num_cols = parsed_result[3]
	list_of_nets = parsed_result[4]

	# error checking
	assert(num_cells)
	assert(num_connections)
	assert(num_rows)
	assert(num_cols)
	assert(list_of_nets)
	# do all cells even fit on the grid
	assert(num_cells <= num_rows*num_cols)

	# create all the cells based on the net connections
	list_of_cells = utility.create_cells(num_cells, num_cols, num_rows, list_of_nets)
	# cross link the cells, each cell is referenced with all the cells it conects to
	list_of_cells = utility.block_X_block(list_of_cells, list_of_nets)
	# cross link the nets with stakeholder cells
	list_of_nets = utility.get_stakeholder_cells_for_net(list_of_nets, list_of_cells)

	# extract the edges and verteces from the nets and cells
	# this allows for ease of use with general graph algorithms
	graph_edges = coarsening.extract_edges(list_of_nets)
	graph_verteces = coarsening.extract_verteces(list_of_cells)
	G = graph.graph(graph_edges, graph_verteces)
		
	# coarsen the graph
	G = coarsening.coarsen_graph(G)

	# after coarsening, constrcut the vertex_X_vertex for fast lookup:
	G.vertex_X_vertex()

	# now, partition the simple graph
	#G = coarse_partition.partition_graph(G)

	# uncoarsen!

	print("uncoarseing now")

	# assign partition to each cell
	list_of_cells = partition.assign_initial_partition(list_of_cells)
	# verify the partition
	partition.verify_partition_count(list_of_cells)

	# compute the initial_cost for reference
	initital_cost = partition.compute_total_cost(list_of_nets, list_of_cells)

	# apply the kernigan_lin algorithm:
	[final_cost, final_list] = partition.kernigan_lin(list_of_cells, list_of_nets)
	# final_cost = KM.kernigan_lin_KM(list_of_cells, list_of_nets)

	# draw the board:
	win = draw.draw_final_result(win, num_cols, num_rows, final_list, list_of_nets)

	# show output statistics
	print('terminating execution, initial cost: ', initital_cost, ' final cost: ', final_cost)

	# this will leave the window open until the user clicks
	win.getMouse()
	win.close()

	return

# command line parser
cmd_parser = argparse.ArgumentParser(description='Process some integers.')
cmd_parser.add_argument('filename', metavar='filename', type=str, nargs='+', help='')
args = cmd_parser.parse_args()

# call the main function using the parsed commands
main(args.filename[0])
