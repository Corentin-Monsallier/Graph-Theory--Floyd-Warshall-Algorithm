import numpy as np
import pandas as pd


def load_txt_file(file_number):
    """
    Load a graph description text file.

    Parameters
    ----------
    file_number : int
        Id of the graph file. The function expects a file named 'graph_{file_number}.txt'.

    Returns
    -------
    list[str]
        List of lines read from the file, including \n characters.
    """
    with open(f'./graphs/graph_{file_number}.txt') as file:
        lines = file.readlines()
    return lines


def parse_graph_file(lines):
    """
    Reads graph informations and edge relations from each file line.

    The file format is expected to follow:
        line 1 : number of vertices
        line 2 : number of arcs
        line 3+ : edges in the form "source_vertex destination_vertex weight"

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
    """
    nb_vertices = int(lines[0])
    nb_arcs = int(lines[1])

    relations = []
    for line in lines[2:]:
        relations.append([int(x) for x in line.strip().split()])  # Remove any space or \n
    
    return nb_vertices, nb_arcs, relations


def adjacency_matrix(nb_vertices, relations):
    """
    Construct the adjacency matrix of a weighted directed graph.

    Parameters
    ----------
    nb_vertices : int
        Number of vertices in the graph.
    relations : list[list[int]]
        List of edges in the format [source_vertex, destination_vertex, weight].

    Returns
    -------
    list[list[int | None]]
        A square adjacency matrix of size nb_vertices * nb_vertices.
        matrix[i][j] contains the edge weight if an edge exists,
        otherwise None.
    """
    matrix = [[None] * nb_vertices for _ in range(nb_vertices)]
    # Depending on the rest of the program, might be better to put float("inf") instead of None and maybe put diagonal of 0 --> don't forget to change documentation
    # matrix = [[float("inf")] * nb_vertices for _ in range(nb_vertices)]
    # for i in range(nb_vertices):
    #    matrix[i][i] = 0
    
    for relation in relations:
        i, j, weight = relation
        matrix[i][j] = weight

    return matrix


def display_matrix(matrix):
    """
    Convert an adjacency matrix into a pandas DataFrame for display.

    Parameters
    ----------
    matrix : list[list[int | None]]
        Adjacency matrix representation of the graph.

    Returns
    -------
    pandas.DataFrame
        DataFrame representation of the matrix for visualization.
    """
    array = np.array(matrix)
    df = pd.DataFrame(data=array)

    print(df)


if __name__ == '__main__':
    graph_1_lines = load_txt_file(file_number=1)
    nb_vertices, nb_arcs, relations = parse_graph_file(graph_1_lines)
    adjacency_matrix_1 = adjacency_matrix(nb_vertices=nb_vertices, relations=relations)
    display_matrix(matrix=adjacency_matrix_1)
