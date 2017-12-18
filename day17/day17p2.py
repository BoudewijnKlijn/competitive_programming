# too slow
import time

start = time.time()

#  puzzle input
steps = 3 # test input
steps = 376

values = [0]
max_insertion = 500000

pos = 0
for insertion in range(1, max_insertion + 1):
    # show progress
    if insertion % 10000 == 0:
        print(insertion)

    pos = (pos + steps) % len(values) + 1
    values.insert(pos, insertion)

end = time.time()
print("%d insertions took %0.4f seconds" % (max_insertion + 1, end - start))

print("Answer part 2:", values[1])

