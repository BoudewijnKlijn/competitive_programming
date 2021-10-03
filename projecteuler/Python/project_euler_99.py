import math


filename = 'p099_base_exp.txt'
with open(filename) as f:
    contents = f.readlines()

greatest_a, greatest_b, greatest_line = None, None, None
for i, line in enumerate(contents):
    a, b = map(int, line.strip().split(','))

    if greatest_a is None:
        greatest_line = i + 1
        greatest_a, greatest_b = a, b
        continue

    if b * math.log(a) > greatest_b * math.log(greatest_a):
        greatest_line = i + 1
        greatest_a, greatest_b = a, b

print(greatest_line)
