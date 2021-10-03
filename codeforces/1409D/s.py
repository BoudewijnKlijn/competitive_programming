import sys
import os

# Read from stdin.
# input = iter(sys.stdin.readlines()).__next__

# Read from file.
if len(sys.argv) > 1:
    if os.path.exists(sys.argv[1]):
        file_name = sys.argv[1]
        with open(file_name, 'r') as f:
            input = iter(f.readlines()).__next__


def get_answer(n: int, s: int) -> int:
    ans = 0
    list_number = [0] + list(map(int, list(str(n))))  # Add one extra zero to beginning of number.
    length = len(list_number)
    pos = length - 1  # Start from the most right digit.
    increased = False
    while sum(list_number) > s:

        # Increase digit until its zero. Only way to decrease sum.
        if list_number[pos] > 0:
            multiplier = length - 1 - pos
            ans += (10 - list_number[pos]) * 10 ** multiplier
            list_number[pos] = 0
            increased = True

        # Also increase one digit to the left with 1. If a 9, keep adding 1 to digits to the left until no longer true.
        if increased:
            while list_number[pos-1] == 9:
                list_number[pos-1] = 0
                pos -= 1
            else:
                list_number[pos-1] += 1

        # Move one digit to the left.
        pos -= 1

    return ans


t = int(input())
for _ in range(t):
    n, s = map(int, input().split())
    print(get_answer(n, s))
