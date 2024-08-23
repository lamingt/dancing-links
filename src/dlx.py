import time
import random


class Node:
    """Class representing a node in the DLX (Dancing Links) matrix."""
    
    def __init__(self, row: int = 0, col: int = 0):
        """
        Initialize a node.

        Args:
            row (int): The row index of the node in the matrix.
            col (int): The column index of the node in the matrix.
        """
        # Initialize node's neighbors
        self.left: Node = self
        self.right: Node = self
        self.up: Node = self
        self.down: Node = self

        # Column header
        self.header: Node = self

        # Row and column index in the matrix
        self.row: int = row
        self.col: int = col

        # Number of nodes in the column
        self.numnodes: int = 0


def link_nodes(matrix: list[list[int]]) -> Node:
    """
    Constructs and links nodes together in a DLX matrix representation.

    Args:
        matrix (list of lists): The matrix representing the problem.

    Returns:
        Node: The header node of the constructed DLX matrix.
    """
    
    NUM_ROW: int = len(matrix)
    NUM_COL: int = len(matrix[0])
    # Create header nodes
    header: Node = Node(-1, -1)
    headers: list[Node] = [Node(-1, col) for col in range(NUM_COL)]

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
    nodes: list[list[Node]] = []
    for i in range(NUM_ROW):
        row_nodes: list[Node] = []
        for j in range(NUM_COL):
            if matrix[i][j]:
                node: Node = Node(i, j)
                node.header = headers[j]
                headers[j].numnodes += 1

                if row_nodes:
                    node.left = row_nodes[-1]
                    row_nodes[-1].right = node

                    # Setting circular defaults in case no more nodes in the row
                    row_nodes[0].left = node
                    node.right = row_nodes[0]
                row_nodes.append(node)

                # Setting circular defaults in case no nodes are below
                node.down = headers[j]
                headers[j].up = node

                # If this is the first node in the column
                if headers[j].down == headers[j]:
                    node.up = headers[j]
                    headers[j].down = node
                elif nodes:
                    found: bool = False
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


def get_min_col(header: Node) -> Node:
    """
    Finds the column header with the minimum number of nodes.

    Args:
        header (Node): The header node of the DLX matrix.

    Returns:
        Node: The column header with the minimum number of nodes.
    """
    cur_header: Node = header.right

    min_col: Node = cur_header
    cur_header = cur_header.right
    while cur_header != header:
        if cur_header.numnodes < min_col.numnodes:
            min_col = cur_header
        cur_header = cur_header.right
    return min_col


def cover(node: Node) -> None:
    """
    Covers a column in the DLX matrix.

    Args:
        node (Node): A node in the column to be covered.
    """
    col_node: Node = node.header

    # Unlinking header from its neighbors
    col_node.left.right = col_node.right
    col_node.right.left = col_node.left

    cur_row: Node = col_node.down
    while cur_row != col_node:
        right_node: Node = cur_row.right
        while right_node != cur_row:
            right_node.up.down = right_node.down
            right_node.down.up = right_node.up

            right_node.header.numnodes -= 1
            right_node = right_node.right
        cur_row = cur_row.down


def uncover(node: Node) -> None:
    """
    Uncovers a column in the DLX matrix.

    Args:
        node (Node): A node in the column to be uncovered.
    """
    col_node: Node = node.header

    cur_row: Node = col_node.up
    while cur_row != col_node:
        left_node: Node = cur_row.left
        while left_node != cur_row:
            left_node.up.down = left_node
            left_node.down.up = left_node

            left_node.header.numnodes += 1
            left_node = left_node.left
        cur_row = cur_row.up

    # Linking header to its neighbors
    col_node.left.right = col_node
    col_node.right.left = col_node


def print_solutions(matrix: list[list[int]], solutions: list[Node]) -> None:
    """
    Prints the solutions found.

    Args:
        matrix (list of lists): The matrix representing the problem.
        solutions (list of Node): The list of nodes representing the solution.
    """
    row_sol = [matrix[node.row] for node in solutions]
    print("Solution found:")
    for row in row_sol:
        print(row)


def search_wrapper(matrix: list[list[int]]) -> None:
    """
    Wrapper function to initialize the DLX matrix and start the search for solutions.

    Args:
        matrix (list of lists): The matrix representing the problem.
    """
    header: Node = link_nodes(matrix)
    solutions: list[Node] = []
    search(0, header, solutions, matrix)


def search(k: int, header: Node, solutions: list[Node], matrix: list[list[int]]) -> None:
    """
    Searches for a solution using Algorithm X.

    Args:
        k (int): The current level of search.
        header (Node): The header node of the DLX matrix.
        solutions (list of Node): The list of nodes representing the current solution.
        matrix (list of lists): The matrix representing the problem.
    """
    if header.right == header:
        print_solutions(matrix, solutions)
        return

    col: Node = get_min_col(header)
    cover(col)

    row: Node = col.down
    while row != col:
        solutions.append(row)

        right_node: Node = row.right
        while right_node != row:
            cover(right_node)
            right_node = right_node.right

        search(k + 1, header, solutions, matrix)

        # If no solution, then remove the solution from the list and uncover the col
        solutions.pop()
        col = row.header
        left_node: Node = row.left
        while left_node != row:
            uncover(left_node)
            left_node = left_node.left

        row = row.down

    uncover(col)


def generate_giant_matrix(rows: int, cols: int) -> list[list[int]]:
    """
    Generates a giant matrix with random binary entries.

    Args:
        rows (int): Number of rows.
        cols (int): Number of columns.

    Returns:
        list of lists: The generated matrix.
    """
    return [[random.randint(0, 1) for _ in range(cols)] for _ in range(rows)]


if __name__ == "__main__":
    Matrix: list[list[int]] = generate_giant_matrix(2000, 21)

    start_time = time.time()

    search_wrapper(Matrix)

    print(f"Search completed in {time.time() - start_time} seconds.")
