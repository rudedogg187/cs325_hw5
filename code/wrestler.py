


def parseInputFile(path):
  with open(path, "r") as f:
    content = f.read().replace("\r", "").split("\n")
    l = len(content)
    i = 0
    data = []
    content.append("-EOF-EOF-EOF-")

    n_lst = []
    r_lst = [] 
    j = i + int(content[i]) 
    i += 1
    while i < j + 1:
      n_lst.append(content[i])
      i += 1

    j = i + int(content[i])
    i += 1
    while i < j + 1:
      r_lst.append(content[i].split(" "))
      i += 1
 
    expected = "\n".join(content[i + 1: -1])

  return [{
    "n_lst": n_lst,
    "r_lst": r_lst,
    "expected": expected

  }]


      
def buildGraph(n_lst, r_lst):
  graph = []
  for n in n_lst:
    lst = set([])
    params = {"dist": float("inf"), "team": -1}
    for rs in r_lst:
      if n in rs:
        for r in rs:
          lst.add(n_lst.index(r))

    i = n_lst.index(n)
    lst.remove(i)
    graph.append([n, lst, params])

  return graph


def printGraph(graph):
  for n in graph:
    lst = []
    for i in n[1]:
      lst.append( graph[i][0] )

    print n[0], lst, n[2]["dist"], n[2]["team"]


def printTeams(graph):
  teams = [[],[]]
  for n in graph:
    teams[n[2]["dist"] % 2].append(n[0])

  print teams 

    #print n[0], lst, n[2]["dist"], n[2]["team"]
  
    
def bfsGraph(graph, i = 0):
  entered = []
  queue = [i]
  d = 0

  graph[i][2]["dist"] = d
  graph[i][2]["team"] = d % 2

  while queue:
    d += 1
    node = queue.pop(0)
    #print "Node: {}".format(graph[node][0])

    # see if wrestler has been looked at yet
    if node not in entered:
      entered.append(node)

      # each rival of current wrestler
      for i in graph[node][1]:
        #print " Rival: {}".format(graph[i][0])
        if graph[i][2]["dist"] == float("inf"):
          graph[i][2]["dist"] = d
          graph[i][2]["team"] = d % 2
          queue.append(i)

    
    if len(queue) == 0 and len(entered) < len(graph):
      for i in range(0, len(graph)):
        if i not in entered:
          queue.append(i)
          break

  x = []    
  for i in range(0, len(entered)):
    x.append(graph[entered[i]][0])
  
  print x
  
    



def main():
  file_path = "input.txt"
  #file_path = raw_input("File Path:\n")
  file_path = "test_files/wrestler2.txt"

  data = parseInputFile(file_path)

  for datum in data:
    graph = buildGraph(datum["n_lst"], datum["r_lst"])
    printGraph(graph)
    print "------"
    bfsGraph(graph)
    print "------"
    printGraph(graph)
    print "------"
    printTeams(graph)

    print "\n---\n{}---".format(datum["expected"])
 
if __name__ == "__main__":
  main()
