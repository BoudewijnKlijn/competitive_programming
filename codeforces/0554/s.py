import sys

from collections import Counter

input = iter(sys.stdin.readlines()).__next__
_ = int(input())
numbers = tuple(map(int, input().split()))
# numbers = tuple(map(int, open('in2', 'r').read().split()))
# numbers = tuple(map(int, open('in3', 'r').read().split()))
# numbers = tuple(map(int, open('in4', 'r').read().split()))

c = Counter(numbers)
numbers = sorted(set(numbers))

# number, chosen bool
scores = dict()
for n in range(max(numbers)+1):
    for chosen in [0, 1]:
        if chosen:
            scores[(n, chosen)] = c.get(n, 0) * n + max(scores.get((n-2, 0), 0), scores.get((n-2, 1), 0))
        else:
            scores[(n, chosen)] = max(scores.get((n-1, 0), 0), scores.get((n-1, 1), 0))

print(max(list(scores.values())))
