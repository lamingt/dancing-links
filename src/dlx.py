import time
import random


class Node:
    """Class representing a node"""

    def __init__(self, row=0, col=0):
        # Initialise nodes neighbours
        self.left = self
        self.right = self
        self.up = self
        self.down = self

        # Column header
        self.header = self

        # Row and column index in the matrix
        self.row = row
        self.col = col

        # Number of nodes in the column
        self.numnodes = 0


# Takes the matrix and links every node with a 1 together in the corresponding DLX matrix,
def link_nodes():
    # Create header nodes
    header = Node(-1, -1)
    headers = [Node(-1, col) for col in range(NUM_COL)]

    # Link headers in a circular linked list
    for i in range(NUM_COL):
        headers[i].header = headers[i]
        headers[i].right = headers[(i + 1) % NUM_COL]
        headers[i].left = headers[(i - 1) % NUM_COL]

    header.right = headers[0]
    headers[0].left = header

    headers[NUM_COL - 1].right = header
    header.left = headers[NUM_COL - 1]

    # Create nodes and link them to headers
    nodes = []
    for i in range(NUM_ROW):
        row_nodes = []
        for j in range(NUM_COL):
            if Matrix[i][j]:
                node = Node(i, j)
                node.header = headers[j]
                headers[j].numnodes += 1

                if row_nodes:
                    node.left = row_nodes[-1]
                    row_nodes[-1].right = node

                    # Setting circular defaults incase no more nodes in the row
                    row_nodes[0].left = node
                    node.right = row_nodes[0]
                row_nodes.append(node)

                # Setting circular defaults incase no nodes are below
                node.down = headers[j]
                headers[j].up = node

                # If this is the first node in the column
                if headers[j].down == headers[j]:
                    node.up = headers[j]
                    headers[j].down = node
                elif nodes:
                    found = False
                    for k in range(len(nodes) - 1, -1, -1):
                        if found:
                            break
                        for m in range(len(nodes[k])):
                            if nodes[k][m].col == node.col:
                                nodes[k][m].down = node
                                node.up = nodes[k][m]
                                found = True
                                break
        nodes.append(row_nodes)

    return header


# Returns the column with the minimum number of nodes
def get_min_col(header):
    cur_header = header.right

    cur_header = header.right
    min_col = cur_header
    cur_header = cur_header.right
    while cur_header != header:
        if cur_header.numnodes < min_col.numnodes:
            min_col = cur_header
        cur_header = cur_header.right
    return min_col


def cover(node):
    col_node = node.header

    # Unlinking header from its neighbours
    col_node.left.right = col_node.right
    col_node.right.left = col_node.left

    cur_row = col_node.down
    while cur_row != col_node:
        right_node = cur_row.right
        while right_node != cur_row:
            right_node.up.down = right_node.down
            right_node.down.up = right_node.up

            right_node.header.numnodes -= 1
            right_node = right_node.right
        cur_row = cur_row.down


def uncover(node):
    col_node = node.header

    cur_row = col_node.up
    while cur_row != col_node:
        left_node = cur_row.left
        while left_node != cur_row:
            left_node.up.down = left_node
            left_node.down.up = left_node

            left_node.header.numnodes += 1
            left_node = left_node.left
        cur_row = cur_row.up

    # Linking header to its neighbours
    col_node.left.right = col_node
    col_node.right.left = col_node


# Prints the solution and the time it took
def print_solutions():
    global SOLUTION_FOUND
    SOLUTION_FOUND = True
    row_sol = [Matrix[node.row] for node in solutions]
    print("Solution found: ")
    for row in row_sol:
        print(row)


def search_wrapper():
    header = link_nodes()
    search(0, header)


# Searching for the solution using Algorithm X
def search(k, header):
    if header.right == header:
        print_solutions()
        return

    col = get_min_col(header)
    cover(col)

    row = col.down
    while row != col:
        solutions.append(row)

        right_node = row.right
        while right_node != row:
            cover(right_node)
            right_node = right_node.right

        search(k + 1, header)

        # If no solution, then remove the solution from the list and uncover the col
        solutions.pop()
        col = row.header
        left_node = row.left
        while left_node != row:
            uncover(left_node)
            left_node = left_node.left

        row = row.down

    uncover(col)


def generate_giant_matrix(rows, cols):
    """
    Generates a giant matrix with random binary entries.
    Args:
        rows (int): Number of rows.
        cols (int): Number of columns.
    Returns:
        list of lists: The giant matrix.
    """
    return [[random.randint(0, 1) for _ in range(cols)] for _ in range(rows)]


# print(generate_giant_matrix(500, 1))
Matrix = generate_giant_matrix(5000, 25)
SOLUTION_FOUND = False
NUM_ROW = len(Matrix)
NUM_COL = len(Matrix[0])

solutions = []

start_time = time.time()

search_wrapper()

# Program exits early if a solution is found
if SOLUTION_FOUND:
    print(f"All solutions found in {time.time() - start_time} seconds.")

else:
    print(f"No solutions found in {time.time() - start_time} seconds.")
