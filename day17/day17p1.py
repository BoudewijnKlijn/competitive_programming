# puzzle input
steps = 3 # test input
steps = 376

values = [0]

pos = 0
for insertion in range(1, 2018):
    pos = (pos + steps) % len(values) + 1
    values.insert(pos, insertion)

print("Answer:", values[values.index(2017) + 1])

