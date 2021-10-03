file = 'C:\\Users\\Admin\\Desktop\\Work\\Learning\\Advent\\day10\\input.txt'
handle = open(file, 'r')
lengths = [ord(x) for x in handle.read().strip()]
lengths += [17, 31, 73, 47, 23]

real_list = list(range(256))
pos = 0
skip_size = 0

for round in range(64):
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

# from sparse hash to dense hash
dense_hash = []
for i in range(256):
    if i % 16 == 0:
        dense_hash.append(real_list[i])
    else:
        dense_hash[-1] = dense_hash[-1] ^ real_list[i]

# format in hexadecimal format
answer = ''
for i in range(16):
    answer += format(dense_hash[i], '02x')

print("Answer: ", answer)
