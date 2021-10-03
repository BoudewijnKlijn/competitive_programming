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
        s = input().strip()

        # Init
        subsequences = [0] * n
        prev_char_of_subsequence = dict()
        prev_char = None
        for i, char in enumerate(s):
            # Different character. Try subsequences starting from 1.
            if char != prev_char:
                subsequence = 1
            # Same character. Try subsequences starting from last subsequence plus 1.
            else:
                subsequence += 1

            # If subsequence already used, the last character in that subsequence has to be different from
            # the current character. Otherwise, increase subsequence to try that one.
            while prev_char_of_subsequence.get(subsequence) == char:
                subsequence += 1

            # Store values and prepare for next char.
            subsequences[i] = subsequence
            prev_char_of_subsequence[subsequence] = char
            prev_char = char

        # Return answer.
        print(max(subsequences))
        print(' '.join(map(str, subsequences)))


if __name__ == '__main__':
    main()
