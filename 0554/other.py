# n = int(input())
# arr = [int(x) for x in input().split()]
arr = tuple(map(int, open('in3', 'r').read().split()))

# maximum value of ai
N = pow(10, 5) + 1

# val stores frequency of each number in arr from 1 to 10^5
val = [0] * N

for i in arr:
    val[i] += 1

# dp[i][j] where i = ak or current number, j = 0 means
# if i was not chosen,  j = 1 means i was chosen
dp = [[0] * 2 for _ in range(N)]

dp[1] = [val[1], 0]

for i in range(2, N):
    for j in range(2):
        if j == 1:
            dp[i][j] = val[i] * i + max(dp[i - 2][0], dp[i - 2][1])
        else:
            dp[i][j] = max(dp[i - 1][0], dp[i - 1][1])

print(max(dp[N - 1][0], dp[N - 1][1]))