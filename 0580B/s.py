"""Goal: find combination of friends such that cumulative friendship factor (s) is maximum with constraint that
difference in money (m) between each friend is less than d."""
import sys
import os


# Read from file.
if len(sys.argv) > 1:
    if os.path.exists((file_name := sys.argv[1])):
        with open(file_name, 'r') as f:
            input = iter(f.readlines()).__next__

n, d = map(int, input().split())
ms, ss = list(), list()
for _ in range(n):
    m, s = map(int, input().split())
    ms.append(m)
    ss.append(s)


# Assume we pick friend with index i. We can determine the range of money that is acceptable. We sum friendship factor
# of all friends within the acceptable money range.

# # Brute force: time limit exceeded.
# cumulative_friendship_factors = list()
# for i, m in enumerate(ms):
#     min_money, max_money = m, m + d - 1
#     cumulative_friendship_factor = sum([s for m2, s in zip(ms, ss) if min_money <= m2 <= max_money])
#     cumulative_friendship_factors.append(cumulative_friendship_factor)
# print(max(cumulative_friendship_factors))  # Answer.


# # Smarter: sort by money.
sorted_low_to_high_by_m = sorted(zip(ms, ss))
ms_sorted_by_m, ss_sorted_by_m = zip(*sorted_low_to_high_by_m)

assert tuple(sorted(ms)) == ms_sorted_by_m

# Brute force with sorting: time limit exceeded.
cumulative_friendship_factors = list()
end_index = 0
for start_index, m1 in enumerate(ms_sorted_by_m):
    # Start the end index search from the end index of the previous run for speed up.
    for end_index, m2 in enumerate(ms_sorted_by_m[end_index:], start=end_index):
        # Break if differences is d or more.
        if m2 >= (m1 + d):
            end_index -= 1
            break

    # Calculate friendship factor with determined indices.
    cumulative_friendship_factor = sum(ss_sorted_by_m[start_index: end_index+1])
    cumulative_friendship_factors.append(cumulative_friendship_factor)

print(max(cumulative_friendship_factors))  # Answer.
