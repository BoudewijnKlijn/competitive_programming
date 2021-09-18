import sys
import os

# # Read from stdin.
# input = iter(sys.stdin.readlines()).__next__

# Read from file.
if len(sys.argv) > 1:
    if os.path.exists((file_name := sys.argv[1])):
        with open(file_name, 'r') as f:
            input = iter(f.readlines()).__next__


n = int(input())
xs, hs = list(), list()
for _ in range(n):
    x, h = map(int, input().split())
    xs.append(x)
    hs.append(h)

occupied = None
count_ = 0
for i, (x, h) in enumerate(zip(xs, hs)):
    # The first tree can always be fell to the left.
    if occupied is None:
        occupied = x
        count_ += 1
        continue
    # The last tree can always be fell to the right.
    elif i == (len(xs) - 1):
        occupied = x + h
        count_ += 1
        continue

    # All other trees (not the first and not the last).
    # Can we fell the tree to the left?
    if x - h > occupied:
        occupied = x
        count_ += 1
    # If not, can we fell it the right?
    elif x + h < xs[i+1]:
        occupied = x + h
        count_ += 1
    # Tree cannot be cut, update occupied with the tree stem.
    else:
        occupied = x

print(count_)
