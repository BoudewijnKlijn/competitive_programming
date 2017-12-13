file = 'input.txt'
handle = open(file, 'r')

checksum = 0

for line in handle:
    numbers = line.split()
    for i in range(len(numbers)):
        for j in range(len(numbers)):
            if i == j:
                continue
            val1 = int(numbers[i])
            val2 = int(numbers[j])
            if val1 % val2 == 0:
                checksum += val1 // val2

print("Checksum:", checksum)
