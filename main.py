import numpy as np
from numpy.linalg import eig
import matplotlib.pyplot as plt
import networkx as nx

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
                counter += 1
        f_read.close()
    except FileNotFoundError:
        print("File not found.")
    


    # generate the image of the graph
    make_graph(matrix, 'images/graph' + str(counter) + '.png')

    # open the file again to append the new matrix
    f = open(filename, 'a')
    
    f.write('<h2>Matrix ' + str(counter) + '</h2>\n\n')
    f.write('<div class="graph-container">\n')
    f.write('<img src="images/graph' + str(counter) + '.png" alt="Graph ' + str(counter) + '">\n\n')
    f.write('<pre class="graph-matrix-data">\n')
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            f.write(str(matrix[i, j]) + ' ')
        f.write("    x<sub>" + str(i) + "</sub> = " + "{:.2f}".format(eigvals[i]))
        f.write('\n')
    f.write('</pre>\n\n')
    f.write('</div>\n')

    f.close()
    


def main():
    while True:
        user_input = input("Matrix size: ") #(e.g. '10' for 10 x 10 matrix)
        if user_input == "exit":
            break
        
        # Check if the input is a positive integer >= 2
        try:
            size = int(user_input)
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

