file = 'C:\\Users\\Admin\\Desktop\\Work\\Learning\\Advent\\day12\\input.txt'
handle = open(file, 'r')

contents = dict()
for line in handle:
    words = line.replace(',', '').split()
    contents[int(words[0])] = [int(x) for x in words[2:]]

total_program = dict()
for loop in range(len(contents)):
    print(loop)

    # init program
    program = dict()
    for i in range(len(contents)):
        program[i] = False
    program[loop] = True

    for run in range(len(contents)):
        for row in range(len(contents)):
            for item in contents[row]:
                if program[item]:
                    program[row] = True

    end_list = []
    for k, v in program.items():
        if v:
            end_list += [k]

    total_program[loop] = end_list

