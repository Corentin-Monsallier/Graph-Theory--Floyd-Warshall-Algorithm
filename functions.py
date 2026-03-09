import numpy as np
import pandas as pd
import math

INF = math.inf

def load_txt_file(file_number):
    '''
    Load a graph description text file.

    Parameters
    ----------
    file_number : int
        Id of the graph file. The function expects a file named 'graph_{file_number}.txt'.

    Returns
    -------
    list[str]
        List of lines read from the file, including \n characters.
    '''
    with open(f'./graphs/graph_{file_number}.txt') as file:
        lines = file.readlines()
    return lines


def parse_graph_file(lines):
    '''
    Reads graph informations and edge relations from each file line.

    The file format is expected to follow:
        line 1 : number of vertices
        line 2 : number of arcs
        line 3+ : edges in the form 'source_vertex destination_vertex weight'

    Parameters
    ----------
    lines : list[str]
        All of the lines from the graph file.

    Returns
    -------
    tuple[int, int, list[list[int]]]
        - nb_vertices : number of vertices
        - nb_arcs : number of arcs
        - relations : list of edges formatted as [source_vertex, destination_vertex, weight]
    '''
    nb_vertices = int(lines[0])
    nb_arcs = int(lines[1])

    relations = []
    for line in lines[2:]:
        # Remove any space or \n
        relations.append([int(x) for x in line.strip().split()])
    
    return nb_vertices, nb_arcs, relations


def adjacency_matrix(nb_vertices, relations):
    '''
    Construct the adjacency matrix of a weighted directed graph.

    Parameters
    ----------
    nb_vertices : int
        Number of vertices in the graph.
    relations : list[list[int]]
        List of edges in the format [source_vertex, destination_vertex, weight].

    Returns
    -------
    list[list[int | float]]
        A square adjacency matrix of size nb_vertices * nb_vertices.
        matrix[i][j] contains the edge weight if an edge exists,
        otherwise 'inf'.
    '''
    # We use INF for non-existant paths because it is considered as an upper bound
    matrix = [[INF] * nb_vertices for _ in range(nb_vertices)]
    for i in range(nb_vertices):
       matrix[i][i] = 0
    
    # Fill the adjacency matrix with the weights from the relations
    for relation in relations:
        i, j, weight = relation
        matrix[i][j] = int(weight)

    return matrix


def format_row(row, row_head, row_header_width, col_widths):
    '''
    Format a single row of the adjacency matrix for aligned display.

    Parameters
    ----------
    row : list[str]
        The row of the matrix already converted to strings.
    row_head : str
        The label of the row (typically the vertex index).
    row_header_width : int
        Width reserved for the row header, used for alignment.
    col_widths : list[int]
        Width of each column, used to right-align each cell.

    Returns
    -------
    str
        A formatted string representing the row, with proper spacing and alignment between columns.
    '''
    # Right align the row header to the specified width
    parts = [row_head.rjust(row_header_width)]
    # Right align each cell in the row according to the specified column width
    for col in range(nb_vertices):
        parts.append(str(row[col]).rjust(col_widths[col]))
    return "   ".join(parts)


def display_matrix(matrix, nb_vertices):
    '''
    Display a formatted adjacency matrix with aligned rows and columns.

    Parameters
    ----------
    matrix : list[list[int | float]]
        The adjacency matrix to display.
    nb_vertices : int
        Number of vertices in the graph, used to generate headers.

    Returns
    -------
    None
    '''
    headers = [str(i) for i in range(nb_vertices)]
    str_matrix = [[str(x) for x in row] for row in matrix]

    # Get max length per column
    col_widths = [
        max(len(str_matrix[r][col]) for r in range(nb_vertices))
        for col in range(nb_vertices)
    ]

    # Get max length between header and values per column
    for col in range(nb_vertices):
        col_widths[col] = max(col_widths[col], len(headers[col]))

    # Get the max witho of all headers so that we can later shift the headers to display them at the right place
    row_header_width = max(len(h) for h in headers)

    # Adjust each header so that it reaches the max length with spaces (on the right)
    aligned_headers = [
        headers[col].rjust(col_widths[col])
        for col in range(nb_vertices)
    ]
    print(" " * row_header_width + "   " + "   ".join(aligned_headers))

    for i in range(nb_vertices):
        print(format_row(row=str_matrix[i], row_head=headers[i], row_header_width=row_header_width, col_widths=col_widths))


def init_matrixes(matrix, nb_vertices, relations):
    '''
    Initialize the distance matrix L and predecessor matrix P used by Floyd–Warshall.

    Parameters
    ----------
    matrix : list[list[int | float]]
        The initial adjacency matrix of the graph, where matrix[i][j] contains
        the weight of the edge i → j, or INF if no edge exists.
    nb_vertices : int
        Number of vertices in the graph.
    relations : list[list[int]]
        List of edges in the format [source_vertex, destination_vertex, weight].

    Returns
    -------
    tuple[list[list[int | float]], list[list[int | None]]]
        L : the initial distance matrix (same object as `matrix`)
        P : the predecessor matrix, where P[i][j] = i if an edge i → j exists,
            otherwise None.
    '''
    L = matrix
    P = [[None] * nb_vertices for _ in range(nb_vertices)]

    # For each direct edge i → j, the predecessor of j is i
    for relation in relations:
        i, j, weight = relation
        P[i][j] = i
    return L, P


def floyd_warshall(matrix, nb_vertices, relations):
    '''
    Compute all‑pairs shortest paths using the Floyd–Warshall algorithm.

    Parameters
    ----------
    matrix : list[list[int | float]]
        The adjacency matrix of the graph, where matrix[i][j] contains the
        weight of the edge i → j, or INF if no edge exists.
    nb_vertices : int
        Number of vertices in the graph.
    relations : list[list[int]]
        List of edges in the format [source_vertex, destination_vertex, weight].
        Used to initialize the predecessor matrix.

    Returns
    -------
    tuple[list[list[int | float]], list[list[int | None]]]
        L : the matrix of shortest path distances between all pairs of vertices.
            After execution, L[i][j] contains the minimum cost from i to j.
        P : the predecessor matrix used to reconstruct shortest paths.
            P[i][j] gives the predecessor of j on the shortest path from i to j,
            or None if no path exists.
    '''
    L, P = init_matrixes(matrix, nb_vertices, relations)
    
    for k in range(nb_vertices):
        for i in range(nb_vertices):
            for j in range(nb_vertices):
                # Check if path i → k → j is shorter than current i → j (with additional check if initial value is INF and if new values not INF)
                if ((L[i][j] == INF or 
                     L[i][j] > (L[i][k] + L[k][j])) 
                     and (L[i][k] != INF and L[k][j] != INF)):
                    # Update shortest distance
                    L[i][j] = L[i][k] + L[k][j]
                    # Update predecessor: predecessor of j becomes predecessor of k→j
                    P[i][j] = P[k][j]
    return L, P


def is_absorbing(L, nb_vertices):
    '''
    Detect whether the graph contains an absorbing circuit
    (negative weight cycle) using the Floyd–Warshall result.

    Parameters
    ----------
    L : list[list[int | float]]
        Distance matrix returned by Floyd-Warshall.

    Returns
    -------
    bool
        True if an absorbing circuit exists, False otherwise.
    '''
    for i in range(nb_vertices):
        if L[i][i] < 0:
            return True 
    return False


def minimum_value_path(initial_vertex, final_vertex, P):
    '''
    Reconstruct the minimum‑value path from vertex i to vertex j using the
    predecessor matrix P produced by the Floyd–Warshall algorithm.

    Parameters
    ----------
    i : int
        Starting vertex.
    j : int
        Ending vertex.
    P : list[list[int | None]]
        Predecessor matrix where P[i][j] gives the predecessor of j on the
        shortest path from i, or None if no predecessor exists.

    Returns
    -------
    list[int] | None
        The ordered list of vertices forming the shortest path from i to j.
        Returns None if no path exists.
    '''
    i, j = initial_vertex, final_vertex
    # If the distance is INF, no path exists between i and j
    if L[i][j] == INF:
        return None
    
    path_list = []
    current = j
    
    # Go backwards from j to i using the predecessor matrix
    while current is not None:
        path_list.append(current)
        if current == i:
            break
        # Move to the predecessor of the current vertex
        current = P[i][current]

    # If there is no predecessor, the path does not exist
    if current is None:
        return None

    # Reverse the list to obtain the path from i to j
    return list(reversed(path_list))

if __name__ == '__main__':
    graph_1_lines = load_txt_file(file_number=3)
    nb_vertices, nb_arcs, relations = parse_graph_file(lines=graph_1_lines)
    print(nb_vertices, nb_arcs, relations)
    adjacency_matrix_1 = adjacency_matrix(nb_vertices=nb_vertices, relations=relations)
    display_matrix(matrix=adjacency_matrix_1, nb_vertices=nb_vertices)
    L, P = floyd_warshall(matrix=adjacency_matrix_1, nb_vertices=nb_vertices, relations=relations)
    if is_absorbing(L=L, nb_vertices=nb_vertices):
        print("The graph contains an absorbing circuit.")
    else:
        print("No absorbing circuit detected.")
        print(minimum_value_path(i=0, j=2, P=P))