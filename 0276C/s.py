import sys
import os


# Read from file.
if len(sys.argv) > 1:
    if os.path.exists((file_name := sys.argv[1])):
        with open(file_name, 'r') as f:
            input = iter(f.readlines()).__next__


n, q = map(int, input().split())
a = map(int, input().split())
idx_counts = [0] * n
for _ in range(q):
    l, r = map(int, input().split())
    for idx in range(l-1, r):
        idx_counts[idx] += 1

ans = sum([a*b for a, b in zip(sorted(a), sorted(idx_counts))])
print(ans)
