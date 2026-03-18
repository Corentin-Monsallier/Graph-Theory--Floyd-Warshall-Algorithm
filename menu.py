from functions import *

def menu():

    matrix = None
    L = None
    P = None
    nb_vertices = None
    relations = None

    while True:
        print("\~~~~~~~~~~ GRAPH MENU ~~~~~~~~~~")
        print("1. Load graph")
        print("2. Display adjacency matrix")
        print("3. Run Floyd-Warshall")
        print("4. Check absorbing circuit")
        print("5. Determine the shortest path")
        print("6. Exit")

        choice = input("Choose an option between 1 and 6: ")

        if choice == '1':
            try:
                file_number = int(input("Enter graph number between 1 and 13: "))
                lines = load_txt_file(file_number)
                nb_vertices, nb_arcs, relations = parse_graph_file(lines)
                matrix = adjacency_matrix(nb_vertices, relations)
                print("Graph loaded")

            except FileNotFoundError:
                print("File not found => Please enter a valid graph number between 1 and 13.")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 13.")

        elif choice == '2':
            if matrix is not None:
                display_matrix(matrix)
            else:
                print("Please load a graph first.")

        elif choice == '6':
            print("Exiting bye bye.")
            break

        else:
            print("ERROR => Please choose a number between 1 and 6.")

''' finir le menu, add sous menu comme display les autres sous graphes etc maybe (faire attention aux cas d'erreurs)'''