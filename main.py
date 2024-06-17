import numpy as np
from numpy.linalg import eig
import matplotlib.pyplot as plt
import networkx as nx
import os

OUTPUT_FILE = 'data.html'

def make_graph(adjacency_matrix, pathName):
    myLabels = {}
    for i in range(len(adjacency_matrix)):
        myLabels[i] = str(i+1)
        
    rows, cols = np.where(adjacency_matrix == 1)
    edges = zip(rows.tolist(), cols.tolist())
    gr = nx.DiGraph()
    gr.add_edges_from(edges)
    nx.draw(gr, node_size=500, labels=myLabels, with_labels=True)
    plt.savefig(pathName)
    # clear the plot
    plt.clf()


def append_matrix(matrix, filename):
    matrix = np.array(matrix)
    eigvals, eigvecs = eig(matrix)
    counter = 0

    try:
        # open the file ones and count the number of matrices present
        f_read = open(filename, 'r')

        # count the number of lines containing '### Matrix'
        for line in f_read.readlines():
            if 'Matrix' in line:
                # extract the matrix number
                counter = int((line.split()[1])[:-5])

                counter += 1
        f_read.close()
    except FileNotFoundError:
        pass


    # generate the image of the graph
    make_graph(matrix, 'images/graph' + str(counter) + '.png')

    # open the file again to append the new matrix
    f = open(filename, 'a')
    
    f.write('<h2>Matrix ' + str(counter) + '</h2>\n\n')
    f.write('<div class="graph-container">\n')
    f.write('<img src="images/graph' + str(counter) + '.png" alt="Graph ' + str(counter) + '">\n\n')
    f.write('<pre class="graph-matrix-data">\n')
    # write the top vertex col numbers
    f.write('    ')
    for i in range(matrix.shape[0]):
        f.write(str(i+1) + '  ')
    f.write('\n')
    f.write('    ' + '_  '*matrix.shape[0] + '\n')
    # start writing the matrix
    for i in range(matrix.shape[0]):
        # write the vertex row number
        f.write(str(i+1) + ' | ')
        # write the row elements
        for j in range(matrix.shape[1]):
            f.write(str(matrix[i, j]) + '  ')
        # add an eigenvalue to the side
        f.write("    x<sub>" + str(i) + "</sub> = " + "{:.2f}".format(eigvals[i]))
        f.write('\n')
    f.write('</pre>\n\n')
    f.write('</div>\n')

    f.close()
    
def delete_matrix(matrix_number, filename):
    f_read = open(filename, 'r')
    lines = f_read.readlines()
    f_read.close()

    f_write = open(filename, 'w')

    found = False
    finishedDeleting = False

    for line in lines:
        if('Matrix ' + str(matrix_number) in line):
            found = True
            
        if found and not finishedDeleting:
            if '</div>' in line:
                finishedDeleting = True
                print('Matrix ' + str(matrix_number) + ' deleted.')
            continue
        f_write.write(line)
    
    f_write.close()

    imageDeleted = False
    # delete the image of the graph
    try:
        os.remove('images/graph' + str(matrix_number) + '.png')
        imageDeleted = True
    except FileNotFoundError:
        pass

    if not imageDeleted:
        print('Image of Matrix ' + str(matrix_number) + ' not found.')
    if not found:
        print('Matrix ' + str(matrix_number) + ' not found.')
        return 
    if not finishedDeleting:
        print('Matrix ' + str(matrix_number) + ' not deleted.')
        return

def main():
    while True:
        user_input = input(">>>") #(e.g. '10' for 10 x 10 matrix)
        if user_input == "exit":
            break

        user_input = user_input.split()

        if len(user_input) != 2:
            print("Invalid input. Valid command: 'add <size>', delete <matrix_number> or 'exit'")
            continue
        
        if user_input[0] == 'delete':
            if user_input[1] == 'all':
                open(OUTPUT_FILE, 'w').close()
                os.system('rm images/*')
                print("All matrices deleted.")
                continue


            try:
                matrix_number = int(user_input[1])
                delete_matrix(matrix_number, OUTPUT_FILE)
            except ValueError:
                print("Invalid input. Please enter a valid matrix number.")
            continue

        # Check if the input is a positive integer >= 2
        try:
            size = int(user_input[1])
            if size < 2:
                print("Invalid input. Please enter a positive integer >= 2.")
        except ValueError:
            print("Invalid input. Please enter a positive integer >= 2.")

        matrix = []
        
        i = 0 

        while i < size:
            line = input()
            # check if the user want to break
            if line == "exit":
                break
            line = line.split()
            if len(line) != size:
                print("Invalid input in row #{}. Please reenter row #{} with {} elements.".format(i+1,i+1,size))
                continue
            try:
                matrix.append([int(x) for x in line])
            except ValueError:
                print("Invalid input in row #{}. Please reenter row #{} using integers only.".format(i+1,i+1))
                continue
            i += 1

        append_matrix(matrix, OUTPUT_FILE)
        
if __name__ == '__main__':
    main()

