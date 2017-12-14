import numpy as np

input_code = 'flqrgnkx' # test input
input_code = 'hfdlxzhv'
test_answer = 8108
total_used = 0

islands = np.zeros((128, 128), dtype=int)

for row in range(128):
    hash_input = input_code + '-' + str(row)

    ### code from day 10 ###
    lengths = [ord(x) for x in hash_input]
    lengths += [17, 31, 73, 47, 23]

    real_list = list(range(256))
    pos = 0
    skip_size = 0

    for round in range(64):
        for length in lengths:
            if pos + length > 256:
                sublist = real_list[pos:] + real_list[:pos + length - 256]
            else:
                sublist = real_list[pos: pos + length]

            sublist.reverse()
            if pos + length > 256:
                real_list[pos:] = sublist[:256 - length - pos]
                real_list[:pos + length - 256] = sublist[256 - length - pos:]
            else:
                real_list[pos: pos + length] = sublist

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

    # print(answer)

    ### end code from day 10 ###

    # format in binary format
    banswer = ''
    for char in answer:
        banswer += format(int(char, 16), '04b')

    total_used += banswer.count('1')

    # create np matrix with 0's and 1's for part 2
    banswer_mat_row = [int(c) for c in banswer]
    islands[row, :] = banswer_mat_row

print("Answer part 1:", total_used)


# determine regions
mat = np.arange(128*128).reshape(128, 128)

# create output file to be analyzed with the script for day 12 part 2
output = ''
for row_id in range(128):
    for col_id in range(128):
        cel = row_id*128 + col_id
        if islands[row_id, col_id] != 0:
            output += str(cel) + ' <-> ' + str(cel) + ', '
            if row_id > 0 and islands[row_id-1, col_id] == 1:
                output += str(mat[row_id-1, col_id]) + ', '
            if row_id < 127 and islands[row_id+1, col_id] == 1:
                output += str(mat[row_id+1, col_id]) + ', '
            if col_id > 0 and islands[row_id, col_id-1] == 1:
                output += str(mat[row_id, col_id-1]) + ', '
            if col_id < 127 and islands[row_id, col_id+1] == 1:
                output += str(mat[row_id, col_id+1]) + ', '
            output += '\n'

filename = 'output.txt'
handle = open(filename, 'w')
handle.write(output)


### code from day 12 part 2 with outer filename (input -> output) and variable name (answer -> regions) ###
def f_extend(v_list):
    for item in v_list:
        for candidate in contents[item]:
            if candidate not in v_list:
                v_list.append(candidate)
                f_extend(v_list)
    return v_list

file = 'C:\\Users\\Admin\\Desktop\\Work\\Learning\\Advent\\output.txt'
handle = open(file, 'r')

contents = dict()
for line in handle:
    words = line.replace(',', '').split()
    contents[int(words[0])] = [int(x) for x in words[2:]]

print(contents)

program = dict()
regions = 0
for k, v_list in contents.items():
    if k not in program.keys():
        v_list += [k]
        v_list = f_extend(v_list)
        regions += 1

        v_list = list(set(v_list))
        for row in v_list:
            program[row] = v_list

print("Answer:", regions)

### end code from day 12 part 2 ###

