file = 'input.txt'
handle = open(file, 'r')

correct_count = 0

for line in handle:
    words = line.split()

    # check if words on line are unique
    for pos in range(len(words)):
        if words[pos] in words[pos+1:]:
            break
        elif pos == len(words)-1:
            correct_count += 1

print(correct_count)
