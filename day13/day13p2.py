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


def severity(delay, answer=0):
    # severity works, but is too slow to come up with a solution. moreover, it gives a wrong answer, because if you get caught in layer 0, answer is still 0
    for layer, depth in contents.items():
        if firewall_pos(depth, layer+delay) == 1:
            answer += depth * layer
    return answer


def caught(delay):
    for layer, depth in contents.items():
        if firewall_pos(depth, layer+delay) == 1:
            return True
    return False


delay = 0
while True:
    if not caught(delay):
        break
    else:
        delay += 1

print("Answer:", delay)
