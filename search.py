# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    print "TinyMaze"
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    dfs = util.Stack()  # Creates a stack structure named dfs
    direction = []  # Direction list stores the next action
    visited = []  # Visited stores the list of nodes already traversed
    start = problem.getStartState()  # Get the starting position of PACMAN

    dfs.push((start, []))  # Push the starting position on the stack
    rem_node = True

    if problem.isGoalState(start):  # Check if starting position is goal position
        return []

    while (rem_node):
        if dfs.isEmpty():  # check if stack is empty
            rem_node = False
            return []

        node, direction = dfs.pop()  # Remove the top elements from stack
        visited.append(node)  # Add the popped node to visited list

        if problem.isGoalState(node):  # Check if the popped node is a goal state
            return direction

        successors_list = problem.getSuccessors(node)  # Get (successor, action, stepCost) from getSuccessors
        # function and store in list
        for successor, action, stepcost in successors_list:
            if (successor not in visited):  # if Successor node is already visited, do nothing
                new_direction = direction + [action]
                dfs.push((successor, new_direction))  # When node not in visited, push node and direction to stack


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    bfs = util.Queue()  # create a queue structure bfs
    direction = []  # Direction list stores the next action
    visited = []  # Visited stores the list of nodes already traversed
    start = problem.getStartState()  # Get the starting position of PACMAN
    if problem.isGoalState(start):
        return []

    bfs.push((start, []))  # Push the starting position on the queue
    rem_node = True

    while (rem_node):
        if bfs.isEmpty():  # Check if queue is empty
            rem_node = False
            return []

        node, direction = bfs.pop()  # Remove the top elements from queue until we find unvisited node
        while(bfs.isEmpty() == False and node in visited):
            node, direction = bfs.pop()  # Remove the top elements from queue

        if (problem.isGoalState(node)):  # Check if the popped node is a goal state
            return direction

        successors_list = problem.getSuccessors(node)  # Get (successor, action, stepCost) from getSuccessors
        # function and store in list

        for successor, action, stepcost in successors_list:
            if (successor not in visited):  # if Successor node is already visited, do nothing
                new_node = direction + [action]
                bfs.push((successor, new_node))

        visited.append(node) # Making node as visited since we visited all it's successors


def uniformCostSearch(problem):
    visited = []
    pq = util.PriorityQueue()      # Create a priority queue data structure called pq
    elem1 = problem.getStartState() # Get the starting position of Pacman
    og = 0
    visited.append(elem1)       # Append the starting position on already traversed list
    path = []
    tpath = []

    while (problem.isGoalState(elem1) == False):    # Expand all the neighbours till goal is reached
        sitr = iter(problem.getSuccessors(elem1))

        for elem in sitr:
            if (elem[0] not in visited):
                path = tpath[:]
                path.append(elem[1])
                g = elem[2] + og
                path.append(g)
                path.append(elem[0])
                pq.push(path, g)

        visited.append(elem1)

        while (pq.isEmpty() == False):  # Extract elements from priority queue till we find unvisited node
            tpath = pq.pop()
            elem1 = tpath.pop()
            og = tpath.pop()
            if(elem1 not in visited):
                break

    return tpath


def nullHeuristic(state, problem=None):
    print "NULL Heuristic"
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the food node that has the lowest combined cost and heuristic first."""
    if(problem.__class__.__name__ == "FoodSearchProblem"):

        visited = []
        pq = util.PriorityQueue()
        elem, foodGrid = problem.getStartState()

        og = 0
        f = 0
        visited.append(elem)
        path = []
        tpath = []
        fpath = []
        state = problem.getStartState()

        while (problem.isGoalState(state) == False):

            state = elem, foodGrid
            sitr = iter(problem.getSuccessors(state));

            #iterating through all the neighbours
            for elem in sitr:
                if (elem[0][0] not in visited):
                    path = tpath[:]
                    path.append(elem[1])
                    state = elem[0][0], foodGrid
                    h = heuristic(state, problem)
                    g = elem[2] + og
                    f = g + h
                    path.append(g)
                    path.append(elem[0][0])
                    pq.push(path, f);

            #Iterating in priority queue until we find unvisited node
            while (pq.isEmpty() == False):
                tpath = pq.pop()
                elem = tpath.pop()
                og = tpath.pop()
                if (elem not in visited):
                    visited.append(elem)
                    break

            if(elem in foodGrid.asList()):
                # Removing the food item eaten during this time
                foodGrid[elem[0]][elem[1]] = False
                fpath.extend(tpath)
                # Delete all the visited lists, priority queues and path lists after 1 food is found to start as fresh from that position
                visited.__delslice__(0, len(visited))
                tpath.__delslice__(0, len(tpath))
                path.__delslice__(0, len(path))
                og = 0
                while (pq.isEmpty() == False):
                    pq.pop()
                    pq.count -= 1
                visited.append(elem)

        return fpath;

    else:
        pq = util.PriorityQueue()  # create a priority queue structure pq
        direction = []  # Direction list stores the next action
        visited = []  # Visited stores the list of nodes already traversed
        start = problem.getStartState()  # Get the starting position of PACMAN
        # f is total cost of g function and h function
        f = 0
        g = 0
        h = 0
        og = 0
        if problem.isGoalState(start):
            return []

        pq.push((start, [], 0), 0)  # Push the starting postion on the stack
        rem_node = True

        #Check for remaining nodes to be processed
        while (rem_node):
            if pq.isEmpty():  # Check if priority queue is empty
                rem_node = False
                return []

            node, direction, og = pq.pop()  # Remove the top elements from queue
            #Keep removing nodes from priority queue until we find unvisited node
            while (pq.isEmpty() == False and node in visited):
                node, direction, og = pq.pop()  # Remove the top elements from queue

            if (problem.isGoalState(node)):  # Check if the popped node is a goal state
                return direction

            successors_list = problem.getSuccessors(node)  # Get (successor, action, stepCost) from getSuccessors
            # function and store in list
            for successor, action, stepcost in successors_list:
                if (successor not in visited):  # if Successor node is already visited, do nothing

                    h = heuristic(successor, problem)
                    new_node = direction + [action]
                    g = stepcost + og
                    f = g + h
                    pq.push((successor, new_node, g), f)
            # Add the parent node to visited list since all it's successors have been visited
            visited.append(node)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
