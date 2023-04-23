from copy import deepcopy

#Dictionary with directional movements
DIRECTIONS = {"U": [-1, 0], "D": [1, 0], "L": [0, -1], "R": [0, 1]}

def sanitise():
    END = [[0,0,0], [0,0,0], [0,0,0]]
    attempts = []
    form = 1
    for row in range(len(END)):
        for column in range(len(END)):
            a = True
            while (a==True):
                try:
                    entered = int(input("What should the element in tile " + str(form) + " be: "))
                    if (entered > 8 or entered < 0 or entered in attempts):
                        print("Make sure the input is a non-repeated integer between 0 and 8. ")
                        continue
                    else:
                        attempts.append(entered)
                    END[row][column] = entered
                    a = False
                except ValueError as ve:
                    print("Input can only be an integer, try again. ")

            form += 1

    return END

print("Pick the tiles in your end state: ")
END = sanitise()

print("END STATE: \n")
print(END)

class Puzzle:
    """Class puzzle, with attributes current and previous node, direction (will be used later on for direction in which
        a tile is moved) and g and h for the heuristic function (g(n) and h(n)) """
    def __init__(self, current_node, previous_node, g, h, dir):
        self.current_node = current_node
        self.previous_node = previous_node
        self.g = g
        self.h = h
        self.dir = dir

    def f(self):
        return self.g + self.h


def getNode(current_state, element):
    """Function to obtain the current node (combination of tiles in the puzzle)"""
    for row in range(len(current_state)):
        if element in current_state[row]:
            return (row, current_state[row].index(element))

def ManhattanDistance(current_state):
    """Calculates the Manhattan Distance from the current state to the end state (h(n))"""
    cost = 0
    for row in range(len(current_state)):
        for col in range(len(current_state[0])):
            pos = getNode(END, current_state[row][col])
            cost += abs(row - pos[0]) + abs(col - pos[1])
    return cost

def getAdjacentNode(node):
    """Function that gets all nodes adjacent to the current state. possible combinations of the puzzle that can be
    achieved with just one move off of the current state) """
    nodes = []
    blank_tile = getNode(node.current_node, 0)

    for dir in DIRECTIONS.keys():
        newPos = (blank_tile[0] + DIRECTIONS[dir][0], blank_tile[1] + DIRECTIONS[dir][1])
        if 0 <= newPos[0] < len(node.current_node) and 0 <= newPos[1] < len(node.current_node[0]):
            newState = deepcopy(node.current_node)
            newState[blank_tile[0]][blank_tile[1]] = node.current_node[newPos[0]][newPos[1]]
            newState[newPos[0]][newPos[1]] = 0
            nodes.append(Puzzle(newState, node.current_node, node.g + 1, ManhattanDistance(newState), dir))

    return nodes

def getBestNode(nodes):
    """Calculates which of the adjacent nodes is the most appropriate so that solution is reached in minimal steps.
    Uses heuristic function. """
    keep = True

    for node in nodes.values():
        if keep or node.f() < best:
            keep = False
            bestNode = node
            best = bestNode.f()
    return bestNode

def Astar(path):
    """Builds the path needed to go from the start state to the goal state, using the best nodes picked by the function
    above."""
    node = path[str(END)]
    branch = list()

    while node.dir:
        branch.append({
            'dir': node.dir,
            'node': node.current_node
        })
        node = path[str(node.previous_node)]
    branch.append({
        'dir': '',
        'node': node.current_node
    })
    branch.reverse()

    return branch

def game(puzzle):
    """Main function, where all the logistic for the puzzle happens. Functions are called to identify the best adjacent
    nodes and to build the path as the loop runs."""
    options = {str(puzzle): Puzzle(puzzle, puzzle, 0, ManhattanDistance(puzzle), "")}
    viable = {}

    while True:
        test_node = getBestNode(options)
        viable[str(test_node.current_node)] = test_node

        if test_node.current_node == END:
            return Astar(viable)

        adj_node = getAdjacentNode(test_node)
        for node in adj_node:
            if str(node.current_node) in viable.keys() or str(node.current_node) in options.keys() and options[
                str(node.current_node)].f() < node.f():
                continue
            options[str(node.current_node)] = node

        del options[str(test_node.current_node)]


if __name__ == '__main__':
    #Start State
    print("Pick the tiles in your start state: ")
    START = sanitise()

    print()
    print('Total steps : ', len(START) - 1)
