file_in = 'C:\\Users\\Admin\\Desktop\\Work\\Learning\\Advent\\day15\\input.txt'
handle = open(file_in, 'r')
contents = handle.read()

factor_a = 16807
factor_b = 48271
divisor = 2147483647

# test starting values
a = 65
b = 8921

# input starting values
a = int(contents.split()[4])
b = int(contents.split()[9])

answer_p1 = 0
for i in range(40000000):

    # show progress
    if i % 500000 == 0:
        print(i)

    a = (a * factor_a) % divisor
    b = (b * factor_b) % divisor

    a_bin = format(a, '032b')
    b_bin = format(b, '032b')

    if a_bin[-16:] == b_bin[-16:]:
        answer_p1 += 1

print(answer_p1)
