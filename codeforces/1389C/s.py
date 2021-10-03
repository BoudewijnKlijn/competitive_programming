"""Good number means left cyclic and right cyclic are the same.
The set of good numbers seems limited:
- Every number of length 2 is good
- A number of any length with only one and the same digit is good.
- A number with alternating digits where begin and end are not the same.
With that in mind we can construct those numbers and see which one gives the longest number."""
import sys
import os

from collections import Counter


# Read from stdin.
# input = iter(sys.stdin.readlines()).__next__

# Read from file.
if len(sys.argv) > 1:
    if os.path.exists(sys.argv[1]):
        file_name = sys.argv[1]
        with open(file_name, 'r') as f:
            input = iter(f.readlines()).__next__


t = int(input())
for _ in range(t):
    string = input().strip()
    length = len(string)

    # Construct number of length 2. This is the baseline. Improve with other strategies
    ans = length - 2

    # Count occurrence of digits. If one digit occurs more than two times, that's a better solution than keeping two
    # different digits.
    c = Counter(string)
    max_count = max(c.values())
    if max_count > 2:
        ans = length - max_count

    # Construct number with alternating digits. With different begin and end.
    # With digits 0-9, there are 10*10 combinations minus 10 where both are the same.
    combinations = [(i, j) for i in range(10) for j in range(10) if i != j]

    for i, j in combinations:
        alternating_sequence_length = 0
        idx = 0
        while True:
            # Find i, starting from idx
            idx = string.find(str(i), idx)
            if idx == -1:
                break
            else:
                alternating_sequence_length += 1

            # Find j, starting from idx
            idx = string.find(str(j), idx)
            if idx == -1:
                # Need to have different start and end. If break here we start and end with i. Subtract 1.
                alternating_sequence_length -= 1
                break
            else:
                alternating_sequence_length += 1

        # Update answer if longer sequence is found.
        if (length - alternating_sequence_length) < ans:
            ans = length - alternating_sequence_length

    # Answer.
    print(ans)
