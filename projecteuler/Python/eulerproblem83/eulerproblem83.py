import numpy as np
import time
start = time.time()

max_col = 80
max_row = 80

filename = 'p083_matrix.txt' 
fin=open(filename,'r')
mylist = []
for i in range(max_row):
	mylist.append(fin.readline())

mylist = [m.replace('\n', '.') for m in mylist]
matrix = np.zeros((max_row, max_col))
for row in range(max_row):
    char = 0
    number = 0
    col = 0
    while (mylist[row][char] != '.'):
        if (mylist[row][char] == ','):
            matrix[row, col] = number
            number = 0
            col += 1
        else:
            number = number*10 + int(mylist[row][char])
        char += 1
    matrix[row, col] = number

max_value = 9999*max_row*max_col
path_matrix = np.ones((max_row, max_col))*max_value
path_matrix[max_row-1, max_col-1] = matrix[max_row-1, max_col-1]
something_changed = True
run = 1
while something_changed:
    print(run)
    something_changed = False
    for row in reversed(range(max_row)):
        for col in reversed(range(max_col)):
            if not (row == max_row and col == max_col):
           
                # check left
                if (col-1 >= 0 and path_matrix[row, col-1] + matrix[row,col] < path_matrix[row, col]):
                    path_matrix[row, col] = path_matrix[row, col-1] + matrix[row,col]
                    something_changed = True
                # check right
                if (col+1 <= max_col-1 and path_matrix[row, col+1] + matrix[row,col] < path_matrix[row, col]):
                    path_matrix[row, col] = path_matrix[row, col+1] + matrix[row,col]
                    something_changed = True
                # check up
                if (row-1 >= 0 and path_matrix[row-1, col] + matrix[row,col] < path_matrix[row, col]):
                    path_matrix[row, col] = path_matrix[row-1, col] + matrix[row,col]
                    something_changed = True
                # check down
                if (row+1 <= max_row-1 and path_matrix[row+1, col] + matrix[row,col] < path_matrix[row, col]):
                    path_matrix[row, col] = path_matrix[row+1, col] + matrix[row,col]
                    something_changed = True
    run += 1

end = time.time()
print("Time:",end-start)
print("Answer:",path_matrix[0, 0])
                    