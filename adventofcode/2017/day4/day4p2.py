file = 'input.txt'
handle = open(file, 'r')

correct_count = 0

for line in handle:
    words = line.split()

    # arrange the letters of all words alphabetically
    for pos in range(len(words)):
        letters = list(words[pos])
        sorted_letters = sorted(letters)
        new_word = ''.join(sorted_letters)
        words[pos] = new_word

    # check if words on line are unique
    for pos in range(len(words)):
        if words[pos] in words[pos+1:]:
            break
        elif pos == len(words)-1:
            correct_count += 1

print(correct_count)
