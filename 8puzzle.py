import random  # imported to create random puzzle
import queue  # imported to use a priority queue with the UCS function
import sys  # imported to increase the recursion limit for Python...due to DFS requiring lots of recursion

# sets the python recursion limit which is usually 1000
sys.setrecursionlimit(50000)

# takes user input to continue to run program or end it
user_run_program = input(
    "Do you wish to run this 8 puzzle search program? Enter 1 for yes or 0 for no:")

# loops while user requests to keep running program
while user_run_program == str(1):
    initial_state_input = input(
        "Use 1-default puzzle, 2-random puzzle, or 3-custom puzzle? Enter a 1, 2, or 3:")

    # these statements determine which type of puzzle the user has requested to use as the initial state
    if initial_state_input == str(1):
        initial_state = [1, 3, 4, 8, 6, 2, 0, 7, 5]  # default puzzle
    elif initial_state_input == str(2):
        # creates a random initial puzzle state
        initial_state = random.sample(range(9), 9)
    elif initial_state_input == str(3):
        initial_state_string = input(
            "Enter a list of 9 distinct numbers between 0 and 8 separated by commas (no spaces):")
        # allows user to input a custom puzzle
        initial_state = [int(i) for i in initial_state_string.split(',')]

    # the goal state we're trying to achieve
    goal_state = [1, 2, 3, 8, 0, 4, 7, 6, 5]

    # these are booleans used to test which moves are legal for a state
    can_move_left = True
    can_move_right = True
    can_move_up = True
    can_move_down = True

    dfs_visited = []  # holds all visited puzzle states
    dfs_queue = []  # holds unvisited puzzle states
    # holds a list of Path objects which is used to recover the path to the goal state
    dfs_parent = []
    dfs_path = []  # this is a list that will hold the goal path directions for printing
    dfs_goal_found = False  # global variable used in DFS to end the recursion

    # function to test if moving left is an option, returns a boolean

    def can_move_left(node):
        # this finds the index of 0 in the array and uses modulo to see if it's in left column
        if node.index(0) % 3 == 0:
            return False
        return True

    # function to test if moving right is an option, returns a boolean

    def can_move_right(node):
        z = {2, 5, 8}  # these are the indexes of the right hand column
        for index in z:
            # gets the index of 0 and checks it against the set of right column indexes
            if node.index(0) == index:
                return False
        return True

    # function to test if moving up is an option, returns a boolean

    def can_move_up(node):
        z = {0, 1, 2}  # these are the indexes of the top row
        for index in z:
            # gets the index of 0 and checks it against the set of top row indexes
            if node.index(0) == index:
                return False
        return True

    # function to test if moving down is an option, returns a boolean

    def can_move_down(node):
        z = {6, 7, 8}  # these are the indexes of the bottom row
        for index in z:
            # gets the index of 0 and checks it against the set of bottom row indexes
            if node.index(0) == index:
                return False
        return True

    # this function takes a puzzle state as a parameter, moves the 0 left, and returns the new puzzle state

    def move_left(node):
        new_node = node[:]  # copies the input parameter to a new node
        x = node.index(0)  # variable to store the current location of 0
        # swaps the 0 with the value to the left of it
        new_node[x], new_node[x-1] = new_node[x-1], new_node[x]
        return new_node

    # this function takes a puzzle state as a parameter, moves the 0 right, and returns the new puzzle state

    def move_right(node):
        new_node = node[:]  # copies the input parameter to a new node
        x = node.index(0)  # variable to store the current location of 0
        # swaps the 0 with the value to the right of it
        new_node[x], new_node[x+1] = new_node[x+1], new_node[x]
        return new_node

    # this function takes a puzzle state as a parameter, moves the 0 up, and returns the new puzzle state

    def move_up(node):
        new_node = node[:]  # copies the input parameter to a new node
        x = node.index(0)  # variable to store the current location of 0
        # swaps the 0 with the value above it
        new_node[x], new_node[x-3] = new_node[x-3], new_node[x]
        return new_node

    # this function takes a puzzle state as a parameter, moves the 0 down, and returns the new puzzle state

    def move_down(node):
        new_node = node[:]  # copies the input parameter to a new node
        x = node.index(0)  # variable to store the current location of 0
        # swaps the 0 with the value below it
        new_node[x], new_node[x+3] = new_node[x+3], new_node[x]
        return new_node

    # this function prints the puzzle state as a matrix. I'm not storing the puzzle as a matrix, so I use modulo and new line to display it

    def print_state(node):
        # this allows me to get the index of the node items
        for idx, x in enumerate(node):
            if idx % 3 == 0:  # this uses module to write a new line every third item for displaying as a matrix
                print("\n")
                print(x, end=' ')  # allows printing values on the same line
            else:
                print(x, end=' ')
        print("\n")

    # this class is for returning the goal path once the goal state is found. It holds the parents of all nodes visited and the direction it took to get there

    class Path:
        def __init__(self, direction="start", parent=None, current=None):
            self.direction = direction  # holds the direction taken to get from parent to child
            self.parent = parent  # holds the parent to the current node
            self.current = current  # holds the current node

    # this is the function for using BFS on the initial puzzle state. It returns the path to the goal state.

    def Breadth_First_Search(node):
        bfs_visited = []  # holds all visited puzzle states
        bfs_queue = []  # holds unvisited puzzle states
        parent = []  # holds a list of Path objects which is used to recover the path to the goal state
        # creates a copy of the puzzle state input parmater
        node_copy = node[:]
        path = []  # this is a list that will hold the goal path directions for printing
        # this initializes the initial puzzle state into the parent list
        parent.append(Path("start", None, node_copy))
        # this adds the initial puzzle state to the queue
        bfs_queue.append(node_copy)
        while bfs_queue:  # this loop runs while there are unvisited puzzle states and the goal state has not been found
            state = bfs_queue.pop(0)
            # print_state(state)
            if state == goal_state:  # tests if the current state is the goal state
                while "start" not in path:  # loops through the parent list of Paths until the initial "start" direction is found
                    for x in parent:  # loops through each Path object in the parent list
                        if x.current == state:  # checks if the current node in the Path object equals the state node
                            # if the current node in Path object equals state node, inserts its direction into path list, this creates path to goal
                            path.insert(0, x.direction)
                            state = x.parent  # this resets the state node to the current node's parent so that each parent can be traversed back to initial state from goal
                return path  # returns the path list which holds the directions taken to goal state
            # appends the current state to the visited list
            bfs_visited.append(state)
            if can_move_down(state):  # checks if the 0 can move down in current state
                # checks if the state after moving down has already been visited or not
                if move_down(state) not in bfs_visited:
                    # if move is legal and state hasn't been visited, adds its direction, parent state, and resulting state to the parents list; used to find goal path later
                    parent.append(Path("D", state, move_down(state)))
                    # appends new state after move to queue
                    bfs_queue.append(move_down(state))
            if can_move_up(state):
                if move_up(state) not in bfs_visited:
                    parent.append(Path("U", state, move_up(state)))
                    bfs_queue.append(move_up(state))
            if can_move_left(state):
                if move_left(state) not in bfs_visited:
                    parent.append(Path("L", state, move_left(state)))
                    bfs_queue.append(move_left(state))
            if can_move_right(state):
                if move_right(state) not in bfs_visited:
                    parent.append(Path("R", state, move_right(state)))
                    bfs_queue.append(move_right(state))
        return path

    # this is the function for using DFS on the initial puzzle state. It returns the path to the goal state.

    def Depth_First_Search(node):
        # this instantiates the global variable created earlier so it can be used inside the function
        global dfs_goal_found
        if dfs_goal_found != True:  # initializes the global variable since it can't be done during initialization above
            dfs_goal_found = False
        # creates a copy of the puzzle state input parmater
        node_copy = node[:]
        # this adds the initial puzzle state to the queue
        dfs_queue.insert(0, node_copy)
        while dfs_queue:  # this loop runs while there are unvisited puzzle states and the goal state has not been found
            state = dfs_queue.pop(0)
            # print_state(state)
            if state == goal_state:  # tests if the current state is the goal state
                # sets the global variable to true so no more states will be created and recursion will end
                dfs_goal_found = True
                while "start" not in dfs_path:  # loops through the parent list of Paths until the initial "start" direction is found
                    for x in dfs_parent:  # loops through each Path object in the parent list
                        if x.current == state:  # checks if the current node in the Path object equals the state node
                            # if the current node in Path object equals state node, inserts its direction into path list, this creates path to goal
                            dfs_path.insert(0, x.direction)
                            state = x.parent  # this resets the state node to the current node's parent so that each parent can be traversed back to initial state from goal
                return dfs_path  # returns the path list which holds the directions taken to goal state

            # appends the current state to the visited list
            dfs_visited.append(state)
            # checks if the 0 can move down in current state and that the goal hasn't already been found
            if can_move_down(state) and not dfs_goal_found:
                # checks if the state after moving down has already been visited or not
                if move_down(state) not in dfs_visited:
                    # if move is legal and state hasn't been visited, adds its direction, parent state, and resulting state to the parents list; used to find goal path later
                    dfs_parent.append(Path("D", state, move_down(state)))
                    # recursive call using the newly created state
                    Depth_First_Search(move_down(state))
            if can_move_up(state) and not dfs_goal_found:
                if move_up(state) not in dfs_visited:
                    dfs_parent.append(Path("U", state, move_up(state)))
                    Depth_First_Search(move_up(state))
            if can_move_left(state) and not dfs_goal_found:
                if move_left(state) not in dfs_visited:
                    dfs_parent.append(Path("L", state, move_left(state)))
                    Depth_First_Search(move_left(state))
            if can_move_right(state) and not dfs_goal_found:
                if move_right(state) not in dfs_visited:
                    dfs_parent.append(Path("R", state, move_right(state)))
                    Depth_First_Search(move_right(state))
        return dfs_path

    # this is the function for using UCS on the initial puzzle state. It returns the path to the goal state.

    def Uniform_Cost_Search(node):
        ucs_visited = []  # holds all visited puzzle states
        ucs_queue = queue.PriorityQueue()  # creates a priority queue for holding states
        parent = []  # holds a list of Path objects which is used to recover the path to the goal state
        # creates a copy of the puzzle state input parmater
        node_copy = node[:]
        path = []  # this is a list that will hold the goal path directions for printing
        # this initializes the initial puzzle state into the parent list
        parent.append(Path("start", None, node_copy))
        # this adds the initial puzzle state to the queue
        # this variable holds the tuple that will be added to the priority queue (0 is the priority); needed b/c put() won't work with node_copy directly
        item = (0, node_copy)
        # this puts the previously created tuple into the priority queue
        ucs_queue.put(item)
        while ucs_queue:  # this loop runs while there are unvisited puzzle states and the goal state has not been found
            # this varaible removes and holds the highest priority state from the queue
            state_temp = ucs_queue.get()
            # this separates the priority queue item that was popped into a priority and state variable
            state_value, state = state_temp
            # print_state(state)
            if state == goal_state:  # tests if the current state is the goal state
                while "start" not in path:  # loops through the parent list of Paths until the initial "start" direction is found
                    for x in parent:  # loops through each Path object in the parent list
                        if x.current == state:  # checks if the current node in the Path object equals the state node
                            # if the current node in Path object equals state node, inserts its direction into path list, this creates path to goal
                            path.insert(0, x.direction)
                            state = x.parent  # this resets the state node to the current node's parent so that each parent can be traversed back to initial state from goal
                return path  # returns the path list which holds the directions taken to goal state
            # appends the current state to the visited list
            ucs_visited.append(state)
            if can_move_down(state):  # checks if the 0 can move down in current state
                # checks if the state after moving down has already been visited or not
                if move_down(state) not in ucs_visited:
                    # if move is legal and state hasn't been visited, adds its direction, parent state, and resulting state to the parents list; used to find goal path later
                    parent.append(Path("D", state, move_down(state)))
                    # creates variable for put() function in next line to increment priority value and hold new state
                    item = (state_value + 1, move_down(state))
                    # puts the updated priority and state into the priority queue
                    ucs_queue.put(item)
            if can_move_up(state):
                if move_up(state) not in ucs_visited:
                    parent.append(Path("U", state, move_up(state)))
                    item = (state_value + 1, move_up(state))
                    ucs_queue.put(item)
            if can_move_left(state):
                if move_left(state) not in ucs_visited:
                    parent.append(Path("L", state, move_left(state)))
                    item = (state_value + 1, move_left(state))
                    ucs_queue.put(item)
            if can_move_right(state):
                if move_right(state) not in ucs_visited:
                    parent.append(Path("R", state, move_right(state)))
                    item = (state_value + 1, move_right(state))
                    ucs_queue.put(item)
        return ucs_queue

    # this section runs the user selected search algorithm and prints the results
    search_algorithm = input(
        "Which search algorithm will be used? (1-BFS, 2-DFS, 3-UCS)? Enter 1, 2, or 3:")
    if search_algorithm == str(1):
        print("\nInitial State for BFS:")
        print_state(initial_state)  # prints initial starting state
        goal_directions_bfs = Breadth_First_Search(
            initial_state)  # stores goal path into variable for printing
        print("Goal Path using BFS:")
        print(goal_directions_bfs,)  # prints goal path
        user_run_program = input(
            "Do you wish to run this 8 puzzle search program again? Enter 1 for yes or 0 for no:")
    elif search_algorithm == str(2):
        print("\nInitial State for DFS:")
        print_state(initial_state)  # prints initial starting state
        dfs_parent.append(Path("start", None, initial_state))
        goal_directions_dfs = Depth_First_Search(
            initial_state)  # stores goal path into variable
        print("Goal Path using DFS:")
        print(goal_directions_dfs,)  # prints goal path
        user_run_program = input(
            "Do you wish to run this 8 puzzle search program again? Enter 1 for yes or 0 for no:")
    elif search_algorithm == str(3):
        print("\nInitial State for UCS:")
        print_state(initial_state)  # prints initial starting state
        goal_directions_ucs = Uniform_Cost_Search(
            initial_state)  # stores goal path into variable
        print("Goal Path using UCS:")
        print(goal_directions_ucs,)  # prints goal path
        user_run_program = input(
            "Do you wish to run this 8 puzzle search program again? Enter 1 for yes or 0 for no:")

else:
    sys.exit()
