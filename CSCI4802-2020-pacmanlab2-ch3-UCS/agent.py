from pacmanGame import *
from maze_graph import *
import sys
sys.path.insert(0, ".\\aima-python-master")
infinity = float('inf')

class SearchAgent:
    def __init__(self, game,sAgent):
        problem=PacmanProblem(game.pacmanPos[0],game.capsulePos, game)
        self.problem=problem;
       # self.game=game
        self.actionSeq=[]
        self.sAgent=sAgent
        self.numVisited=0

    def dfs(self):
        node=Node(self.problem.initial)
        if self.problem.goal_test(node.state):
            return node.solution()
        frontier=Stack()
        frontier.append(node)
        explored=set()
        while True:
            if len(frontier)==0:
                return None
            node=frontier.pop()
            self.numVisited +=1
            if (node not in explored):
                explored.add(node.state)
                if self.problem.goal_test(node.state): # do goal_test only the time it is explored
                    return node.solution()
                for action in self.problem.actions(node.state):
                    child=node.child_node(self.problem, action)
                    if(child.state not in explored):
                        frontier.append(child)

    def uniform_cost_search(self):
        node = Node(self.problem.initial)
        if self.problem.goal_test(node.state):
            return node.solution()
        frontier = PriorityQueue(min, lambda node: node.path_cost)
        frontier.append(node)
        explored = set()
        while True:
            pass
        return None

    def get_actions(self):
        if (len(self.actionSeq) == 0):
            self.problem.initial = self.problem.game.pacmanPos[0]
            if(self.sAgent=="bfs"):
                self.actionSeq=self.bfs()
            elif (self.sAgent=="dfs"):
                self.actionSeq = self.dfs()
            elif (self.sAgent=="ucs"):
                self.actionSeq=self.uniform_cost_search()

    def get_action(self):
        if (len(self.actionSeq) > 0):
            new_pos = self.actionSeq.pop(0)
            action = getDirection(prev, new_pos)
            return (action, new_pos)
        return (None, prev)


    def get_action(self):
        if (len(self.actionSeq) == 0):
            self.problem.initial = self.problem.game.pacmanPos[0]
            if(self.sAgent=="bfs"):
                self.actionSeq=self.bfs()
            elif (self.sAgent=="dfs"):
                self.actionSeq = self.dfs()
            elif (self.sAgent=="uc"):
                self.actionSeq=self.uniform_cost_search()
        prev = self.problem.game.pacmanPos[0]
        if (len(self.actionSeq) > 0):
            new_pos = self.actionSeq.pop(0)
            action = getDirection(prev, new_pos)
            return (action, new_pos)
        return (None, prev)

class PacmanProblem():
    def __init__(self, initial, goal, game):
        self.initial=initial
        self.goal=goal
        self.game=game

        mz = MazeGraph(game)
        mz.genGraph()
        self.graph=mz.graph
        self.costs = mz.edgeCosts

    def actions(self, A):
        """The actions at a graph node are just its neighbors."""
        return list(self.graph.get(A).keys())

    def result(self, state, action):
        """The result of going to a neighbor is just that neighbor."""
        return action

    def path_cost(self, cost_so_far, A,action, B):
        return cost_so_far + (self.graph.get(A, B) or infinity)

    def goal_test(self, state):
        if(state in self.goal):
            return True
        else:
            return False


# ______________________________________________________________________________


class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node {}>".format(self.state)

    def __lt__(self, node):
        return self.state < node.state

    def expand(self, problem):
        """List the nodes reachable in one step from this node."""
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        """[Figure 3.10]"""
        next = problem.result(self.state, action)
        return Node(next, self, action,
                    problem.path_cost(self.path_cost, self.state,
                                      action, next))

    def solution(self):
        """Return the sequence of actions to go from the root to this node."""
        return [node.action for node in self.path()[1:]]

    def path(self):
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    # We want for a queue of nodes in breadth_first_search or
    # astar_search to have no duplicated states, so we treat nodes
    # with the same state as equal. [Problem: this may not be what you
    # want in other contexts.]

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        return hash(self.state)

class Graph:

    """A graph connects nodes (verticies) by edges (links).  Each edge can also
    have a length associated with it.  The constructor call is something like:
        g = Graph({'A': {'B': 1, 'C': 2})
    this makes a graph with 3 nodes, A, B, and C, with an edge of length 1 from
    A to B,  and an edge of length 2 from A to C.  You can also do:
        g = Graph({'A': {'B': 1, 'C': 2}, directed=False)
    This makes an undirected graph, so inverse links are also added. The graph
    stays undirected; if you add more links with g.connect('B', 'C', 3), then
    inverse link is also added.  You can use g.nodes() to get a list of nodes,
    g.get('A') to get a dict of links out of A, and g.get('A', 'B') to get the
    length of the link from A to B.  'Lengths' can actually be any object at
    all, and nodes can be any hashable object."""

    def __init__(self, dict=None, directed=True):
        self.dict = dict or {}
        self.directed = directed
        if not directed:
            self.make_undirected()

    def make_undirected(self):
        """Make a digraph into an undirected graph by adding symmetric edges."""
        for a in list(self.dict.keys()):
            for (b, dist) in self.dict[a].items():
                self.connect1(b, a, dist)

    def connect(self, A, B, distance=1):
        """Add a link from A and B of given distance, and also add the inverse
        link if the graph is undirected."""
        self.connect1(A, B, distance)
        if not self.directed:
            self.connect1(B, A, distance)

    def connect1(self, A, B, distance):
        """Add a link from A to B of given distance, in one direction only."""
        self.dict.setdefault(A, {})[B] = distance

    def get(self, a, b=None):
        """Return a link distance or a dict of {node: distance} entries.
        .get(a,b) returns the distance or None;
        .get(a) returns a dict of {node: distance} entries, possibly {}."""
        links = self.dict.setdefault(a, {})
        if b is None:
            return links
        else:
            return links.get(b)

    def nodes(self):
        """Return a list of nodes in the graph."""
        return list(self.dict.keys())

def UndirectedGraph(dict=None):
    """Build a Graph where every edge (including future ones) goes both ways."""
    return Graph(dict=dict, directed=False)