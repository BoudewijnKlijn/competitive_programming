file = 'C:\\Users\\Admin\\Desktop\\Work\\Learning\\Advent\\day7\\input.txt'
handle = open(file, 'r')

tower = dict()
# weight is for part 2
weight = dict()
multi_weight = dict()
for line in handle:
    parts = line.split()
    weight[parts[0]] = int(parts[1][1:-1])
    if len(parts) < 4:
        value = None
        multi_weight[parts[0]] = [int(parts[1][1:-1])]
    else:
        value = list()
        for i in range(3, len(parts)):
            value.append(parts[i].replace(',', ''))
    tower[parts[0]] = value


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

while needle not in multi_weight.keys():
    for k, v in tower.items():
        if v is None:
            continue

        try:
            value = [weight[k]]
            for sub in v:
                value.append(sum(multi_weight[sub]))
            multi_weight[k] = value
        except:
            continue

error_keys = list()
for k, v in multi_weight.items():
    if len(v) == 1:
        continue

    for i in range(1, len(v)-1):
        if v[i] != v[i+1] and k not in error_keys:
            error_keys.append(k)

for key in error_keys:
    print("Key:", key, tower[key], "Weights", multi_weight[key])

print("Answer:", weight['ycbgx'] - 5)
