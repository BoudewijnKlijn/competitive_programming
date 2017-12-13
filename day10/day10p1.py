file = 'C:\\Users\\Admin\\Desktop\\Work\\Learning\\Advent\\day10\\input.txt'
handle = open(file, 'r')
lengths = [int(x) for x in handle.read().strip().split(',')]

real_list = list(range(256))
pos = 0
skip_size = 0
for length in lengths:
    if pos + length > 256:
        sublist = real_list[pos:] + real_list[:pos+length-256]
    else:
        sublist = real_list[pos: pos+length]

    sublist.reverse()
    if pos + length > 256:
        real_list[pos:] = sublist[:256-length-pos]
        real_list[:pos+length-256] = sublist[256-length-pos:]
    else:
        real_list[pos: pos+length] = sublist

    pos = (pos + length + skip_size) % 256
    skip_size += 1

print("Answer: ", real_list[0]*real_list[1])
