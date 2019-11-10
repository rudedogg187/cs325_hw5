import sys


#################################
# Parse .txt input file
#################################
def parseInputFile(path):
  #try to open the file and read its content
  try:
    with open(path, "r") as f:
      content = f.read().replace("\r", "").split("\n")

  # if unable to open file, return null 
  except:
    return None

  # if able to open file, parse it
  l = len(content)
  # iterator for file content
  i = 0
  # lst to store each set of rivalires
  data = []
  # add a file termination flag to flag file's end
  content.append("-EOF-EOF-EOF-")
 
  # go through file until a blank line, or term flag is reached 
  while content[i] != '' and content[i] != "-EOF-EOF-EOF-": 
    # declare a node list
    n_lst = []
    # declare a rivalry lst
    r_lst = [] 
    # where rivalies should start 
    j = i + int(content[i]) 
    i += 1
    # iterate nodes, add to node list
    while i < j + 1:
      n_lst.append(content[i])
      i += 1
    # where rivalies should start 
    j = i + int(content[i])
    i += 1
    # iterate rivals, add to rival lst
    while i < j + 1:
      r_lst.append(content[i].split(" "))
      i += 1

    # save to var the expect output string 
    expected = "\n".join(content[i + 1: -1])

    # append the parsed data to the data lst
    data.append({
      "n_lst": n_lst,
      "r_lst": r_lst,
      "expected": expected
    })

  #return the parsed data
  return data


#################################
# Build graph from input file content
#################################
def buildGraph(n_lst, r_lst):
  # declare a dict to be an adj lst
  graph = {}
  # iterate all the nodes in the node list
  for n in n_lst:
    # delare a set to store node's neighbors
    adjs = set([])
    # delare distance to be infinity
    dist = float("inf")
    # declare team to be -1
    team = -1
    # iterat all rivalries
    for rs in r_lst:
      # if the current node is in the rivalry set
      if n in rs:
        # go through the rivals in the set
        for r in rs:
          # if the rival is not the current node
          if r != n:
            # add the node to the adjacny list
            adjs.add(r)

    # add each entry to the graph
    graph[n] = { "adjs": adjs, "dist": dist, "team": team }

  # return the compete adjacency lst
  return graph


#################################
# Print graph
#################################
def printGraph(graph):
  for node in graph:
    print node
    print graph[node]
    print


#################################
# Breadth First Search graph
#################################
def bfsGraph(graph, nodes):
  # declare a two team lst, use sets so team members are unique
  teams = [set([]), set([])]
  # while there are nodes to be looked at
  while nodes:
    # grab the first node in the node lst
    node = nodes[0]
    # distance shall be 0 since this is a starting node
    dist = 0
    # create a queue, and add the node to that queue
    queue = [node]
    # create a list of nodes that have been looked at
    entered = []

    # set the node's distance to the current distance (0)
    graph[node]["dist"] = dist
    # set the node's team to 1 or 0 - modulus of its disance to start node
    graph[node]["team"] = dist % 2
    # add the node to the approriat team set
    teams[(dist) % 2].add(node)

    # while there are nodes in the queue
    while queue:
      # grab the node in index 1 of the queue
      node = queue.pop(0)
      # save this node's distance to the dist var
      dist = graph[node]["dist"]
  
      # pop this node out of the node list (this is needed for disconnect graphs) 
      nodes.pop( nodes.index(node) )

      # if the node has yet to be looked at, proceed
      if node not in entered:
        # add the node to the looked at lst
        entered.append(node)

        # grab all of the node's neighbors
        adjs = graph[node]["adjs"]

        # iterate each of the node's neighbors
        for adj in adjs:
          # add the neighbor to the approriate team set
          # if dataset is impossible, member will be added to 2 teams
          teams[(dist + 1) % 2].add(adj)

          # if the neighbor is not in quue and it's distance has yet to be set then proceed
          if adj not in queue and graph[adj]["dist"] == float("inf"):
            # set the neighbor's distance to one greater than it's parent            
            graph[adj]["dist"] = dist + 1
            # set the node's team to the mod of it's distance 
            graph[adj]["team"] = (dist + 1) % 2

         #   teams[(dist + 1) % 2].add(adj)
            # plunk the neighbor into the queue
            queue.append(adj)

  # return the teams
  return teams


#################################
# Print teams to console
#################################
def printTeams(teams, node_count):
  # Team names
  names = ["Babyfaces:", "Heels:    "]
  # Track total member count, if count > node_count then team not valid
  member_count = 0
  # Text string to build the console output
  text = ""
  # iterate through the teams
  for i in range(0, len(teams)):
    # increment the member count by then teams length
    member_count += len(teams[i])
    # add team name and team members to output string
    text += "{}  {}\n".format(names[ i %2], " ".join(teams[i]))

  # check to see if member_count != node count, if so - not valid
  if member_count != node_count:
    # change text output to impossible in this case
    text = "Impossible"
  
  # print the teams (or impossible) to console
  print "\n{}\n".format(text)



#################################
# Main function
#################################
def main():
  # Input File path
  # if input file was not given via cmd line, ask for file
  if len(sys.argv) == 1:
    file_path = raw_input("File Path:\n")

  # input file was given via cmd line
  else:
    file_path = sys.argv[1]

  # Parse Input File
  data = parseInputFile(file_path)

  # If File Not Found
  if data == None:
    print "\n{} could not be located\n".format(file_path)
    exit(0)

  # File Was Found
  # Iterate through datasets in the file
  for datum in data:
    # Get an adjacency list for current set
    graph = buildGraph(datum["n_lst"], datum["r_lst"])
    # Save the node list for the set
    nodes = datum["n_lst"]
    # Store the number of nodes in the set (used to see if teams are valid)
    node_count = len(nodes)
    #printGraph(graph)
    # Perform BFS to build teams
    teams = bfsGraph(graph, nodes)
    # Print teams 
    printTeams(teams, node_count)
    #print "\n---\n{}---".format(datum["expected"])

    exit(0)

if __name__ == "__main__":
  main()
