
import edge
import vertex
import graph

def extract_edges(list_of_nets):
  graph_edges = []

  # for all the nets, extrace each edge
  for cur_net in list_of_nets:
    # error checking
    assert(cur_net.connections)

    # create the edges
    for cur_connection in cur_net.connections:
      graph_edges.append(edge.edge(cur_net.root, cur_connection))
      assert(cur_net.root is not cur_connection)

  # return all the edges
  return graph_edges

def extract_verteces(list_of_cells):
  graph_verteces = []

  # for all the cells, extrace each vertex
  for cur_cell in list_of_cells:
    graph_verteces.append(vertex.vertex(cur_cell.id))
    
  # return all the verteces
  return graph_verteces

'''
TODO
we need more than 1 iteration to find the maximal matching
'''
def find_maximal_matching(input_graph):

  # list of edges in the maximal matching
  maximal_matching = []

  graph_edges = input_graph.edges

  # add the correct edges to the maximal matching: greedy algorithm
  for cur_edge in graph_edges:
    if cur_edge not in maximal_matching:
      can_add_cur_edge = True
      for compare_edge in maximal_matching:
        # can we add cur_edge to maximal_matching?
        if ((cur_edge.node_0 is compare_edge.node_0) 
          or (cur_edge.node_0 is compare_edge.node_1)
          or (cur_edge.node_1 is compare_edge.node_0) 
          or (cur_edge.node_1 is compare_edge.node_1)):
          can_add_cur_edge = False
          break
      if can_add_cur_edge:
        maximal_matching.append(cur_edge)

  return maximal_matching

# collapses all edges in the maximal matching
def collapse_max_matching(maximal_matching, G):

  '''
  print("maximal_matching size: ", len(maximal_matching))
  print("maximal matching:")
  for edge in maximal_matching:
    edge.to_string()
  print("Done with maximal matching")
  '''
  
  # setup work for the collapsing
  # remove the edges
  for cur_edge in maximal_matching:
    G.removed_edges.append(cur_edge)
    G.edges.remove(cur_edge)
  
  # do the collapsing and update the graph accordingly
  for cur_edge in maximal_matching:
    G.collapse_verteces(cur_edge.node_0, cur_edge.node_1)

  return G
    


def coarsen_graph(G):

  print("Graph before coarsening: ")
  #G.to_string_verbose()
  G.print_stats()

  # coarsened graph
  new_list_of_cells = []
  new_list_of_nets = []

  # do the actual coarsening!
  
  for i in range(5):
    # find maximal matching
    maximal_matching = find_maximal_matching(G)

    if (maximal_matching):
      G = collapse_max_matching(maximal_matching, G)
      print("coarsening step: ", i)
      G.print_stats()

  # debugging - print the graph
  print("Graph after coarsening: ")
  G.print_stats()

  # return the new graph
  return G
