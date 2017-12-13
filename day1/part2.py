filename = 'input.txt'
inputs = open(filename, 'r')

agg = 0
for line in inputs:
    half = len(line)//2
    for i in range(len(line)):
        comp = (i + half) % len(line)
        if i < len(line)-1 and line[i] == line[comp]:
            agg += int(line[i])
        elif i == len(line)-1 and line[i] == line[comp]:
            agg += int(line[i])

print("Answer:", agg)
