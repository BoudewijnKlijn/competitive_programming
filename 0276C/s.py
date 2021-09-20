import sys
import os
from collections import Counter


# Read from file.
if len(sys.argv) > 1:
    if os.path.exists(sys.argv[1]):
        file_name = sys.argv[1]
        with open(file_name, 'r') as f:
            input = iter(f.readlines()).__next__

# Read and store input.
n, q = map(int, input().split())
a = map(int, input().split())
ls, rs = list(), list()
for _ in range(q):
    l, r = map(int, input().split())
    ls.append(l)
    rs.append(r)

# Count how many times l and r were mentioned.
count_l = Counter(ls)
count_r = Counter(rs)

# Everytime an l is mentioned we increase with one, and everytime an r is mentioned we decrease with one for the next.
value = 0
idx_counts = dict()
for idx in range(1, n+1):
    value += count_l.get(idx, 0) - count_r.get(idx-1, 0)
    idx_counts[idx] = value

# Multiply the largest number with the most mentioned idx, etc.
ans = sum([ai*bi for ai, bi in zip(sorted(a, reverse=True), sorted(idx_counts.values(), reverse=True))])
print(ans)
