import numpy as np
from numpy.linalg import eig

OUTPUT_FILE = 'data.md'

def append_matrix(matrix, filename):
    matrix = np.array(matrix)
    eigvals, eigvecs = eig(matrix)
    counter = 0

    # open the file ones and count the number of matrices present
    f_read = open(filename, 'r')
    # counte the number of lines containing '### Matrix'
    for line in f_read.readlines():
        if '### Matrix' in line:
            counter += 1
    f_read.close()

    # open the file again to append the new matrix
    f = open(filename, 'a')
    
    f.write('### Matrix ' + str(counter) + '\n\n')
    f.write('<pre>\n')
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            f.write(str(matrix[i, j]) + ' ')
        f.write("    x<sub>" + str(i) + "</sub> = " + "{:.2f}".format(eigvals[i]))
        f.write('\n')
    f.write('</pre>\n\n')

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

