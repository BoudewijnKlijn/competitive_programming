file = 'C:\\Users\\Admin\\Desktop\\Work\\Learning\\Advent\\day11\\input.txt'
handle = open(file, 'r')
steps = handle.read().strip().split(',')

directions = ['n', 'ne', 'se', 's', 'sw', 'nw']
counter_directions = directions[3:] + directions[:3]
counter_directions_2 = [[directions[(i-1) % 6], directions[(i+1) % 6]] for i in range(6)]
dir_dict = dict(list(zip(directions, counter_directions)))
dir_dict_2 = dict(list(zip(directions, counter_directions_2)))
count_dirs = [0, 0, 0, 0, 0, 0]

for direction in directions:
    print(steps.count(direction))


end_reached = False
while not end_reached:
    i = 0
    while i < len(steps):
        step = steps[i]
        if dir_dict_2[step][0] in steps and dir_dict_2[step][1] in steps:
            steps.remove(step)
            steps.remove(dir_dict_2[step][0])
            steps.remove(dir_dict_2[step][1])
            break
        i += 1

    if i >= len(steps):
        end_reached = True

end_reached = False
while not end_reached:
    i = 0
    while i < len(steps):
        step = steps[i]
        if dir_dict[step] in steps:
            steps.remove(step)
            steps.remove(dir_dict[step])
            break
        i += 1

    if i >= len(steps):
        end_reached = True
