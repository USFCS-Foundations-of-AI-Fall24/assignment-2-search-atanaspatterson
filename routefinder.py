from math import sqrt
from queue import PriorityQueue
from Graph import Graph
from Graph import Node
from Graph import Edge


class map_state() :
    ## f = total estimated cost
    ## g = cost so far
    ## h = estimated cost to goal
    def __init__(self, location="", mars_graph=None,
                 prev_state=None, g=0,h=0):
        self.location = location
        self.mars_graph = read_mars_graph("MarsMap")
        self.prev_state = prev_state
        self.g = g
        self.h = h
        self.f = self.g + self.h

    def __eq__(self, other):
        return self.location == other.location

    def __hash__(self):
        return hash(self.location)

    def __repr__(self):
        return "(%s)" % (self.location)

    def __lt__(self, other):
        return self.f < other.f

    def __le__(self, other):
        return self.f <= other.f

    def is_goal(self):
        return self.location == '1,1'


def a_star(start_state, heuristic_fn, goal_test, use_closed_list=True) :
    search_queue = PriorityQueue()
    closed_list = {}
    num_states = 0
    search_queue.put(start_state)
    graph = start_state.mars_graph

    if use_closed_list :
        closed_list[start_state] = True
    
    while not search_queue.empty():
        next_state = search_queue.get()
        if goal_test(next_state):
            print("Goal found")
            print(next_state)
            print()
            ptr = next_state.prev_state
            while ptr is not None :
                print(ptr)
                ptr = ptr.prev_state
            print("Number of states generated = {}".format(num_states))
            return next_state
        else : 
            edges = next_state.mars_graph.get_edges(Node(next_state.location))
            successors = []
            for edge in edges: # create new state, append f and the state to successors
                new_state = map_state(location=edge.dest, mars_graph=graph, prev_state=next_state)
                new_state.g = next_state.g + edge.val 
                new_state.h = heuristic_fn(new_state)
                new_state.f = new_state.g + new_state.h
                successors.append((new_state.f, new_state))
            num_states += len(successors)
            if use_closed_list :
                successors = [item for item in successors
                                    if item[1] not in closed_list]
                for s in successors :
                    closed_list[s[1]] = True
            for successor in successors:
                search_queue.put(successor[1])



## default heuristic - we can use this to implement uniform cost search
def h1(state) :
    return 0

## you do this - return the straight-line distance between the state and (1,1)
def sld(state) :
    coordinates = state.location.split(",")
    return sqrt((int(coordinates[0]) - 1) ** 2 + ((int(coordinates[1]) - 1) ** 2))

## you implement this. Open the file filename, read in each line,
## construct a Graph object and assign it to self.mars_graph().
def read_mars_graph(filename):

    with open(filename, 'r') as file:
        lines = file.readlines()
        graph = Graph()
        for line in lines:
            node_string = line.split(":")[0]
            adjacent_nodes = line.split(":")[1].split(" ")
            adjacent_nodes.remove("")
            adjacent_nodes[-1]= adjacent_nodes[-1].strip("\n")
            node = Node(node_string)
            edge_list = [Edge(node, x, 1) for x in adjacent_nodes]
            graph.add_node(node)
            for edge in edge_list:
                graph.add_edge(edge)

        return graph
            
            

if __name__=="__main__" :
    file = "MarsMap"
    test_state = map_state()
    # print(test_state.mars_graph)
    test_state.location = "4,6"
    # print(sld(test_state))
    test_state.location = "8,8"
    goal_test = lambda state: state.is_goal()# had to find online - didn't work normally
    a_star(test_state, sld, goal_test)

    a_star(test_state, h1, goal_test)
    
        



