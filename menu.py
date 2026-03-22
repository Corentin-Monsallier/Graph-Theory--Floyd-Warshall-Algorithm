from functions import *

def FW_submenu(L, P, nb_vertices) -> None :
    '''
    Display a submenu for visualizing the results of the Floyd–Warshall algorithm.

    This submenu allows the user to:
        - Display the distance matrix L
        - Display the predecessor matrix P
        - Return to the main menu

    Parameters
    ----------
    L : list[list[int | float]]
        Distance matrix computed by Floyd–Warshall.
    P : list[list[int | None]]
        Predecessor matrix used to reconstruct shortest paths.
    nb_vertices : int
        Number of vertices in the graph.

    Returns
    -------
    None
    '''
    while True:
        print("\n~~~~~~~~~~ FLOYD-WARSHALL SUBMENU ~~~~~~~~~~\n")
        print("1. Display L matrix")
        print("2. Display P matrix")
        print("3. Back to main menu\n")

        choice = input("Choose an option between 1 and 3: ")

        if choice == '1':
            print("DEBUG L:", L)
            display_matrix(L, nb_vertices)
        elif choice == '2':
            display_matrix(P, nb_vertices)
        elif choice == '3':
            break
        else:
            print("ERROR => Please choose a number between 1 and 3.")

def menu() -> None :

    '''
    Main interactive menu for the graph application.

    This menu allows the user to:
        1. Load a graph from a file
        2. Display its adjacency matrix
        3. Run the Floyd–Warshall algorithm
        4. Check for an absorbing circuit (negative cycle)
        5. Compute the shortest path between two vertices
        6. Exit the program

    The function manages user input, error handling, and calls
    the appropriate functions from the functions module.

    Returns
    -------
    None
    '''

    global L
    matrix = None
    L = None
    P = None
    nb_vertices = None
    relations = None

    while True:
        print("\n~~~~~~~~~~ GRAPH MENU ~~~~~~~~~~\n")
        print("1. Load graph")
        print("2. Display adjacency matrix")
        print("3. Run Floyd-Warshall")
        print("4. Check absorbing circuit")
        print("5. Determine the shortest path")
        print("6. Exit\n")

        choice = input("Choose an option between 1 and 6: ")

        ###### LOAD GRAPH ######
        if choice == '1':
            try:
                file_number = int(input("Enter graph number between 1 and 13: "))
                lines = load_txt_file(file_number)
                nb_vertices, nb_arcs, relations = parse_graph_file(lines)
                print("NB_VERTICES:", nb_vertices)
                print("RELATIONS:", relations)
                matrix = adjacency_matrix(nb_vertices, relations)
                
                L,P = None, None
                print("Graph loaded")

            except FileNotFoundError:
                print("File not found => Please enter a valid graph number between 1 and 13.")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 13.")
        
        ###### DISPLAY ADJACENCY MATRIX ######
        elif choice == '2':
            if matrix is not None:
                display_matrix(matrix, nb_vertices)
            else:
                print("Please load a graph first.")

        ###### RUN FLOYD-WARSHALL ######
        elif choice == '3':
            if matrix is None:
                print("Please load a graph first.")
                continue
            try:
                L, P = floyd_warshall(matrix, nb_vertices, relations)

                print("\nFINAL L:")
                display_matrix(L, nb_vertices)

                print("\nFINAL P:")
                display_matrix(P, nb_vertices)

                FW_submenu(L, P, nb_vertices)

            except Exception as e:
                print("ERROR during Floyd-Warshall:", e)

        ###### CHECK ABSORBING CIRCUIT ###### 
        elif choice == '4':
            if L is None:
                print("Run Floyd-Warshall first.")
            else:
                if is_absorbing(L, nb_vertices):
                    print("The graph has an absorbing circuit.")
                else:
                    print("The graph does not have an absorbing circuit.")

        ###### DETERMINE SHORTEST PATH ######
        elif choice == '5':
            if L is None:
                print("Run Floyd-Warshall first.")
                continue
            elif is_absorbing(L, nb_vertices) == True:
                print("Cannot determine shortest path due to absorbing circuit.")
                continue
            try:
                # We ask the user for the start and end vertices, ensuring they are valid integers within the range of vertices
                i = int(input(f"Enter start vertex (0 to {nb_vertices-1}): "))
                j = int(input(f"Enter end vertex (0 to {nb_vertices-1}): "))

                if i < 0 or i >= nb_vertices or j < 0 or j >= nb_vertices:
                    print("Invalid vertices.")
                    continue
                # We call the minimum_value_path function to get the shortest path from vertex i to vertex j using the predecessor matrix P and the distance matrix L
                path = minimum_value_path(i, j, P, L)

                if path is None:
                    print("No path exists.")
                else:
                    print("Shortest path:", " -> ".join(map(str, path)))
                    print("Cost:", L[i][j])

            except ValueError:
                print("Error: Please enter valid integer vertices.")

        ###### EXIT PROGRAM ######      
        elif choice == '6':
            print("Exiting bye bye !")
            break

        else:
            print("ERROR => Please choose a number between 1 and 6.")

if __name__ == "__main__":
    menu()
