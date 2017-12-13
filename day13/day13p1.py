file = 'C:\\Users\\Admin\\Desktop\\Work\\Learning\\Advent\\day13\\input.txt'
handle = open(file, 'r')

contents = dict()
for line in handle:
    words = line.replace(':', '').split()
    contents[int(words[0])] = int(words[1])


def firewall_pos(depth, time):
    cycle = list(range(1, depth)) + list(range(depth, 1, -1))
    cycle_length = (depth-1) * 2
    cycle_index = time % cycle_length
    return cycle[cycle_index]


answer = 0
for layer, depth in contents.items():
    if firewall_pos(depth, layer) == 1:
        answer += depth * layer
print("Answer:", answer)
