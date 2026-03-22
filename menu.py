from functions import *

def FW_submenu(L, P, nb_vertices):
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

#def shortest_path_submenu(P, nb_vertices):


def menu():

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

        elif choice == '2':
            if matrix is not None:
                display_matrix(matrix, nb_vertices)
            else:
                print("Please load a graph first.")

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
        
        elif choice == '4':
            if L is None:
                print("Run Floyd-Warshall first.")
            else:
                if is_absorbing(L, nb_vertices):
                    print("The graph has an absorbing circuit.")
                else:
                    print("The graph does not have an absorbing circuit.")

        elif choice == '5':
            if matrix is not None:
                #shortest_path_submenu(P, nb_vertices)
                print("This feature is not implemented yet.")
            else:
                print("Please load a graph first.")

        elif choice == '6':
            print("Exiting bye bye !")
            break

        else:
            print("ERROR => Please choose a number between 1 and 6.")

if __name__ == "__main__":
    menu()
''' finir le menu, add sous menu comme display les autres sous graphes etc maybe (faire attention aux cas d'erreurs)'''