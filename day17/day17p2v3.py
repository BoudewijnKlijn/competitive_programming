# smarter approach: it doesn't matter where or what we insert as long as it is not at position 1.
# just keep track of that position
import time

start = time.time()

#  puzzle input
steps = 376

max_insertion = 50000000

pos = 0
pos_1 = None
length = 1
for insertion in range(1, max_insertion + 1):
    pos = (pos + steps) % length + 1
    if pos == 1:
        pos_1 = insertion
    length += 1

end = time.time()
print("Took %0.4f seconds" % (end - start))

print("Answer part 2:", pos_1)

