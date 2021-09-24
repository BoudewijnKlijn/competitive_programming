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


def is_solvable_v3(n, a, b):
    """Smart way: Analyze numbers in modulo form.
    If remainder goal is 1, we can just keep adding b to get to n.
    Otherwise, make more remainders from starting point (which is 1).
    Adding b doesn't change the remainder (since we do mod b). Multiplying with a might change the remainder."""
    # What is the remainder we need to achieve
    remainder_goal = n % b

    # Keep track of number and remainders that are checked already.
    number = 1
    remainders_checked = set()
    while True:
        remainder = number % b

        if remainder_goal == remainder:
            return True

        # If remainder already checked, it's impossible.
        if remainder in remainders_checked:
            return False
        else:
            remainders_checked.add(remainder)

        # We need to arrive at correct remainder before numbers are bigger than the goal.
        number *= a
        if number > n:
            return False


def main():
    t = int(input())
    for _ in range(t):
        n, a, b = map(int, input().split())
        if is_solvable_v3(n, a, b):
            print("Yes")
        else:
            print("No")


if __name__ == '__main__':
    main()

