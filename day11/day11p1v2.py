file = 'C:\\Users\\Admin\\Desktop\\Work\\Learning\\Advent\\day11\\input.txt'
handle = open(file, 'r')
steps = handle.read().strip().split(',')

directions = ['n', 'ne', 'se', 's', 'sw', 'nw']
ns_values = [1, 0.5, -0.5, -1, -0.5, 0.5]
ew_values = [0, 1, 1, 0, -1, -1]
values = list(zip(ns_values, ew_values))
dir_values = dict(list(zip(directions, values)))

ns_value_count = 0
ew_value_count = 0
for step in steps:
    ns_value_count += dir_values[step][0]
    ew_value_count += dir_values[step][1]

print(ns_value_count, ew_value_count)
print("Answer:", (abs(ns_value_count) - abs(ew_value_count) * 0.5) + abs(ew_value_count))
