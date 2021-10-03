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


def main():
    t = int(input())
    for _ in range(t):
        n = int(input())
        s = list(map(int, input().strip()))

        # Init
        subsequences = [0] * n
        max_subsequence = 0
        last_used_zero = list()  # store subsequences where zero was used as last number
        last_used_one = list()  # store subsequences where one was used as last number
        for i, char in enumerate(s):
            if char == 0:
                try:
                    # Get a subsequence where a one was used as last number.
                    subsequence = last_used_one.pop()
                except IndexError:
                    # If no subsequence has a one as last, make a new subsequence. It must not exist yet, so take max
                    # and increase with 1.
                    subsequence = max_subsequence + 1
                    max_subsequence += 1
                last_used_zero.append(subsequence)
            # Same approach for ones.
            elif char == 1:
                try:
                    subsequence = last_used_zero.pop()
                except IndexError:
                    subsequence = max_subsequence + 1
                    max_subsequence += 1
                last_used_one.append(subsequence)
            else:
                raise ValueError()

            # Store value.
            subsequences[i] = subsequence

        # Return answer.
        print(max(subsequences))
        print(' '.join(map(str, subsequences)))


if __name__ == '__main__':
    main()
