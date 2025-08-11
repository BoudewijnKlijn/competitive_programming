t = 10000
tests = ['10000']


added = 0
length = 1
while added < t:
    for i in range(2 ** length):
        added += 1
        string = f'{i:b}'.zfill(length)
        tests.append(f'\n{length}')
        tests.append(f'\n{string[::-1]}')
        if added == t:
            break
    length += 1


with open('in2', 'w') as f:
    f.writelines(tests)
