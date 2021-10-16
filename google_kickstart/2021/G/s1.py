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

T = int(input())
for t in range(1, T + 1):
    ans = 'YES'
    N, D, C, M = map(int, input().split())
    S = list(input().strip())

    dogs_remaining = S.count('D')
    for ai in S:
        is_dog = ai == 'D'
        if dogs_remaining == 0:
            break
        elif is_dog and D > 0:
            D -= 1
            C += M
            dogs_remaining -= 1
            continue
        elif not is_dog and C > 0:
            C -= 1
            continue
        else:
            ans = 'NO'
            break

    # print answer
    print(f'Case #{t}: {ans}')
