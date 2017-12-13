file = 'input.txt'
handle = open(file, 'r')

checksum = 0

for line in handle:
    numbers = line.split()
    linemax = None
    linemin = None
    for sval in numbers:
        try:
            ival = int(sval)
        except:
            print("Error")
        if linemin is None:
            linemin = ival
            linemax = ival
        elif ival < linemin:
            linemin = ival
        elif ival > linemax:
            linemax = ival
    checksum += linemax - linemin

print("Checksum:", checksum)
