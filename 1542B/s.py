import sys
import os

from collections import deque

# Read from stdin.
# input = iter(sys.stdin.readlines()).__next__

# Read from file.
if len(sys.argv) > 1:
    if os.path.exists(sys.argv[1]):
        file_name = sys.argv[1]
        with open(file_name, 'r') as f:
            input = iter(f.readlines()).__next__


def is_solvable(n, a, b):
    """Start from n and see if we can go back to 1."""
    numbers = deque([n])
    while numbers:
        number = numbers.popleft()
        print(numbers)
        print(number)
        if number == 1:
            return True
        if a != 1 and number % a == 0:
            numbers.append(number // a)
        if number - b >= 1:
            numbers.append(number - b)
    return False


def is_solvable_v2(n, a, b):
    """Start from 1 and see if we can reach n."""
    numbers = [1]
    number_set = {1}
    idx = 0
    while True:
        try:
            number = numbers[idx]
            idx += 1
        except IndexError:
            return False

        if a > 1:
            new = number * a
            if new == n:
                print(numbers)
                return True
            elif new <= n and new not in number_set:
                numbers.append(new)
                number_set.add(new)

        new = number + b
        if new == n:
            print(numbers)
            return True
        elif new <= n and new not in number_set:
            numbers.append(new)
            number_set.add(new)


def main():
    t = int(input())
    for _ in range(t):
        n, a, b = map(int, input().split())
        if is_solvable_v2(n, a, b):
            print("Yes")
        else:
            print("No")


if __name__ == '__main__':
    main()

