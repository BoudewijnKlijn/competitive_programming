import sys
import os


# Read from file.
if len(sys.argv) > 1:
    if os.path.exists((file_name := sys.argv[1])):
        with open(file_name, 'r') as f:
            input = iter(f.readlines()).__next__


# Gather inputs.
t = int(input())
n_list, a_list = list(), list()
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    n_list.append(n)
    a_list.append(a)

# Loop over testcases.
for n, a in zip(n_list, a_list):

    max_number = None
    current_time = 0
    for i, ai in enumerate(a):
        if max_number is None:
            max_number = ai
            continue
        elif ai > max_number:
            max_number = ai

        difference_with_max_number_before = ai - max_number

        # If larger number before we have to increase time.
        # Can subtract increments that were used for others. Sum of all previous is current one minus 1, due to
        # increments with power of 2.
        difference_with_max_number_before += 2 ** current_time - 1

        while difference_with_max_number_before < 0:
            current_time += 1
            difference_with_max_number_before += 2 ** (current_time - 1)

    # Answer.
    print(current_time)
