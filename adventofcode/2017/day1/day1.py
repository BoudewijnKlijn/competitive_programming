filename = 'input.txt'
inputs = open(filename, 'r')

agg = 0
for line in inputs:
    for i in range(len(line)):
        if i < len(line)-1 and line[i] == line[i+1]:
            agg += int(line[i])
        elif i == len(line)-1 and line[i] == line[0]:
            agg += int(line[i])

print("Answer:", agg)
