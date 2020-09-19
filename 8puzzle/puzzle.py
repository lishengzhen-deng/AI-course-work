
from __future__ import division
from __future__ import print_function

import sys
import math
import time
import json
import queue as Q
import resource

#### SKELETON CODE ####
## The Class that Represents the Puzzle
class PuzzleState(object):
    """
        The PuzzleState stores a board configuration and implements
        movement instructions to generate valid children.
    """
    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        """
        :param config->List : Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        """
        if n*n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")
        if set(config) != set(range(n*n)):
            raise Exception("Config contains invalid/duplicate entries : ", config)

        self.n        = n
        self.cost     = cost
        self.parent   = parent
        self.action   = action
        self.config   = config
        self.children = []

        # Get the index and (row, col) of empty block
        self.blank_index = self.config.index(0)
        self.blank_postion = (math.floor(self.blank_index/self.n), self.blank_index%self.n)

    def display(self):
        """ Display this Puzzle state as a n*n board """
        for i in range(self.n):
            print(self.config[3*i : 3*(i+1)])

    def move_up(self):
        """
        Moves the blank tile one row up.
        :return a PuzzleState with the new configuration
        """
        if self.blank_postion[0] == 0:
            return None
        up_position = (self.blank_postion[0] - 1, self.blank_postion[1])
        up_index = up_position[0] * 3 + up_position[1]
        new_config = self.config[:]
        new_config[self.blank_index],new_config[up_index] = self.config[up_index], 0
        up_state = PuzzleState(config=new_config,n=self.n,parent=self,action="Up",cost=self.cost + 1)
        return up_state

    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """
        if self.blank_postion[0] == self.n - 1:
            return None
        down_position = (self.blank_postion[0] + 1, self.blank_postion[1])
        down_index = down_position[0] * 3 + down_position[1]
        new_config = self.config[:]
        new_config[self.blank_index],new_config[down_index] = self.config[down_index], 0
        down_state = PuzzleState(config=new_config,n=self.n,parent=self,action="Down",cost=self.cost + 1)
        return down_state

    def move_left(self):
        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """
        if self.blank_postion[1] == 0:
            return None
        left_position = (self.blank_postion[0], self.blank_postion[1] - 1)
        left_index = left_position[0] * 3 + left_position[1]
        new_config = self.config[:]
        new_config[self.blank_index],new_config[left_index] = self.config[left_index], 0
        left_state = PuzzleState(config=new_config,n=self.n,parent=self,action="Left",cost=self.cost + 1)
        return left_state

    def move_right(self):
        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """
        if self.blank_postion[1] == self.n - 1:
            return None
        right_position = (self.blank_postion[0], self.blank_postion[1] + 1)
        right_index = right_position[0] * 3 + right_position[1]
        new_config = self.config[:]
        new_config[self.blank_index],new_config[right_index] = self.config[right_index], 0
        right_state = PuzzleState(config=new_config,n=self.n,parent=self,action="Right",cost=self.cost + 1)
        return right_state

    def expand(self):
        """ Generate the child nodes of this node """

        # Node has already been expanded
        if len(self.children) != 0:
            return self.children

        # Add child nodes in order of UDLR
        children = [
            self.move_up(),
            self.move_down(),
            self.move_left(),
            self.move_right()]

        # Compose self.children of all non-None children states
        self.children = [state for state in children if state is not None]
        return self.children

    def __eq__(self, other):
        # use to define whether state equal or not, used in ' in set ' judgement
        if not isinstance(other, PuzzleState):
            return NotImplemented
        return self.config == other.config

    def __hash__(self):
        # list cannot be hash directly
        return hash(str(self.config))

    def __lt__(self, other):
        # compare which state is more bigger , __cmp__ in python 2.x
        return 0

# Function that Writes to output.txt
class Frontier(object):
    """
        The PuzzleState stores a board configuration and implements
        movement instructions to generate valid children.
    """
    def __init__(self, type):
        self.type = type
        if type == "queue":
            self.q = Q.Queue()
        elif type == "lifo":
            self.q = Q.LifoQueue()
        elif type == "priority":
            self.q = Q.PriorityQueue()
        self.s = set()

    def put(self, item):
        self.q.put(item)
        if self.type == "priority":
            self.s.add(item[1])
        else:
            self.s.add(item)

    def get(self):
        item = self.q.get()
        if self.type == "priority":
            self.s.remove(item[1])
        else:
            self.s.remove(item)
        return item

    def empty(self):
        return self.q.empty() and len(self.s) == 0

### Students need to change the method to have the corresponding parameters
def writeOutput(results):
    ### Student Code Goes here
    file1 = open("output.txt", "w+")
    for key in results.keys():
        sentence = key+": "+str(results[key])+'\n'
        file1.write(sentence)
    file1.close()
    pass

def bfs_search(initial_state):
    """BFS search"""
    frontier = Frontier("queue")
    visited = set()
    frontier.put(initial_state)
    max_depth = 0
    while not frontier.empty():
        state = frontier.get()
        visited.add(state)
        # state.display()
        # print("------------",test_goal(state))
        if test_goal(state):
            cop = state.cost
            start = "Initial"
            path_to_goal = []
            while state.action != start:
                path_to_goal.insert(0,state.action)
                state = state.parent
            result = {
                "path_to_goal": path_to_goal,
                "cost_of_path": cop,
                "nodes_expanded": len(visited) - 1,
                "search_depth": cop,
                "max_search_depth": max_depth
            }
            return result
        else:
            neighbor = state.expand()
            if state.cost + 1 > max_depth:
                max_depth = state.cost + 1
            for next in neighbor:
                if next not in visited and next not in frontier.s:
                    frontier.put(next)
    return None

def dfs_search(initial_state):
    """DFS search"""
    frontier = Frontier("lifo")
    visited = set()
    frontier.put(initial_state)
    max_depth = 0
    while not frontier.empty():
        state = frontier.get()
        if state.cost > max_depth:
            max_depth = state.cost
        visited.add(state)
        # state.display()
        # print("------------",test_goal(state))
        if test_goal(state):
            cop = state.cost
            start = "Initial"
            path_to_goal = []
            while state.action != start:
                path_to_goal.insert(0,state.action)
                state = state.parent
            result = {
                "path_to_goal": path_to_goal,
                "cost_of_path": cop,
                "nodes_expanded": len(visited) - 1,
                "search_depth": cop,
                "max_search_depth": max_depth
            }
            return result
        else:
            neighbor = state.expand()
            for i in range(len(neighbor)-1, -1, -1):
                if neighbor[i] not in visited and neighbor[i] not in frontier.s:
                    frontier.put(neighbor[i])
    return None

def A_star_search(initial_state):
    """A * search"""
    frontier = Frontier("priority")
    visited = set()
    cost = calculate_total_cost(initial_state)
    frontier.put((cost,initial_state))
    max_depth = 0
    while not frontier.empty():
        state = frontier.get()[1]
        if state.cost > max_depth:
            max_depth = state.cost
        visited.add(state)
        # state.display()
        # print("------------",test_goal(state))
        if test_goal(state):
            cop = state.cost
            start = "Initial"
            path_to_goal = []
            while state.action != start:
                path_to_goal.insert(0,state.action)
                state = state.parent
            result = {
                "path_to_goal": path_to_goal,
                "cost_of_path": cop,
                "nodes_expanded": len(visited) - 1,
                "search_depth": cop,
                "max_search_depth": max_depth
            }
            return result
        else:
            neighbor = state.expand()
            for i in range(len(neighbor) - 1, -1, -1):
                if neighbor[i] not in visited and neighbor[i] not in frontier.s:
                    cost = calculate_total_cost(neighbor[i])
                    frontier.put((cost,neighbor[i]))
    return None

def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    ### STUDENT CODE GOES HERE ###
    n = state.n
    manhattan_dis = 0
    for i in range(n**2):
        manhattan_dis += calculate_manhattan_dist(i,state.config[i],n)
    return state.cost + manhattan_dis

def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""
    ### STUDENT CODE GOES HERE ###
    cur_pos = (math.floor(idx/n), idx%n)
    sup_pos = (math.floor(value/n), value%n)
    return abs(cur_pos[0] - sup_pos[0]) + abs(cur_pos[1] - sup_pos[1])

def test_goal(puzzle_state):
    """test the state is the goal state or not"""
    board_size = puzzle_state.n
    goal_state = []
    for i in range(board_size**2):
        goal_state.append(i)
    return puzzle_state.config == goal_state

# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    # search_mode = sys.argv[1].lower()
    # begin_state = sys.argv[2].split(",")
    search_mode = "ast"
    begin_state = [8,6,4,2,1,3,5,7,0]
    begin_state = list(map(int, begin_state))
    board_size  = int(math.sqrt(len(begin_state)))
    hard_state  = PuzzleState(begin_state, board_size)
    start_time  = time.time()
    start_mem = resource.getrusage(resource.RUSAGE_SELF)[2]
    res = {}

    if   search_mode == "bfs": res = bfs_search(hard_state)
    elif search_mode == "dfs": res = dfs_search(hard_state)
    elif search_mode == "ast": res = A_star_search(hard_state)
    else:
        print("Enter valid command arguments !")

    end_time = time.time()
    end_mem = resource.getrusage(resource.RUSAGE_SELF)[2]

    print("Program completed in %f second(s)"%(end_time-start_time))
    print("Memory usage: %f" % ((end_mem - start_mem)/1024))

    res["running_time"] = round(end_time-start_time, 8)
    res["max_ram_usage"] = round((end_mem - start_mem)/(1024*1024),8)

    for key in res.keys():
        print(key,": ",res[key])
    writeOutput(res)

if __name__ == '__main__':
    main()