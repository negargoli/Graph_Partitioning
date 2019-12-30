import net

#
# Parses the input file
#
# Return the num_cells, num_connections, num_rows, num_cols from the input file
#
def parse_file(filename):
  # open the file    
  inputfile = open(filename)
  
  # parse the first line
  first_line = inputfile.readline()
  first_line = first_line.split()

  num_cells = int(first_line[0])
  num_connections = int(first_line[1])
  num_rows = int(first_line[2])
  num_cols = int(first_line[3])
  
  # parse the nets
  list_of_nets = []
  for i in range(num_connections):
    cur_net_unparsed = inputfile.readline().split()

    cur_net = net.net(int(cur_net_unparsed[1]), int(cur_net_unparsed[0])-1)

    for j in range(2, int(cur_net_unparsed[0])+1):
      cur_net.add_connection(int(cur_net_unparsed[j]))

    # error checking, did we parse correctly?
    # print(len(cur_net.connections), cur_net.num_connections)
    assert(len(cur_net.connections) == cur_net.num_connections)
    list_of_nets.append(cur_net)

  # error checking
  # print(len(list_of_nets), num_cells)
  assert(len(list_of_nets) == num_connections)
  
  # returned the parsed information
  return [num_cells, num_connections, num_rows, num_cols, list_of_nets]