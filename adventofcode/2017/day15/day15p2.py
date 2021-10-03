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

# judge 5 million pairs
judged = 0
answer_p2 = 0
while judged < 5000000:

    # show progress
    if judged % 500000 == 0:
        print(judged)

    a = (a * factor_a) % divisor
    while a % 4 != 0:
        a = (a * factor_a) % divisor

    b = (b * factor_b) % divisor
    while b % 8 != 0:
        b = (b * factor_b) % divisor

    a_bin = bin(a)
    b_bin = bin(b)
    if a_bin[-16:] == b_bin[-16:]:
        answer_p2 += 1
    judged += 1

print(answer_p2)
