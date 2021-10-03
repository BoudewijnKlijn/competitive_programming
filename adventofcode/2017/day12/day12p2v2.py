def f_extend(v_list):
    for item in v_list:
        for candidate in contents[item]:
            if candidate not in v_list:
                v_list.append(candidate)
                f_extend(v_list)
    return v_list

file = 'C:\\Users\\Admin\\Desktop\\Work\\Learning\\Advent\\day12\\input.txt'
handle = open(file, 'r')

contents = dict()
for line in handle:
    words = line.replace(',', '').split()
    contents[int(words[0])] = [int(x) for x in words[2:]]

program = dict()
answer = 0
for k, v_list in contents.items():
    if k not in program.keys():
        v_list += [k]
        v_list = f_extend(v_list)
        answer += 1

        v_list = list(set(v_list))
        for row in v_list:
            program[row] = v_list

print("Answer:", answer)
