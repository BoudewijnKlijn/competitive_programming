# I think this should scale better, but still way too slow.
import numpy as np
import time

start = time.time()

#  puzzle input
steps = 3 # test input
steps = 376

max_insertion = 500000
values = np.zeros(max_insertion+1, dtype=int)

pos = 0
length = 1
for insertion in range(1, max_insertion+1):

    # show progress
    if insertion % 10000 == 0:
        print(insertion)

    pos = (pos + steps) % length + 1
    values[pos+1: length+1] = values[pos: length]
    values[pos] = insertion
    length += 1

end = time.time()
print("%d insertions took %0.4f seconds" % (max_insertion+1, end-start))

item_index = np.where(values == max_insertion)[0][0]
print("Answer part 1:", values[item_index+1])
print("Answer part 2:", values[1])
