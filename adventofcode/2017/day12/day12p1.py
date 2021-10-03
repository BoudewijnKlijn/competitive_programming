file = 'C:\\Users\\Admin\\Desktop\\Work\\Learning\\Advent\\day12\\input.txt'
handle = open(file, 'r')

contents = dict()
program = dict()

for line in handle:
    words = line.replace(',', '').split()
    contents[int(words[0])] = [int(x) for x in words[2:]]

# init program
for i in range(len(contents)):
    program[i] = False
program[0] = True

for run in range(len(contents)):
    for row in range(len(contents)):
        for item in contents[row]:
            if program[item]:
                program[row] = True

answer = 0
for k, v in program.items():
    if v:
        answer += 1

print("Answer:", answer)
