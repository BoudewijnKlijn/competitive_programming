file = 'C:\\Users\\Admin\\Desktop\\Work\\Learning\\Advent\\day7\\input.txt'
handle = open(file, 'r')

tower = dict()
for line in handle:
    parts = line.split()
    if len(parts) < 4:
        value = None
    else:
        value = list()
        for i in range(3, len(parts)):
            value.append(parts[i].replace(',', ''))
    tower[parts[0]] = value

# print(tower)

bottom_found = False
needle = None

while not bottom_found:
    bottom_found = True

    for k, v in tower.items():

        if needle is None:
            needle = k
            continue

        if v is not None and needle in v:
            needle = k
            bottom_found = False
            break

print("Bottom:", needle)
