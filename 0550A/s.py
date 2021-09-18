string = input()
# string = open('in', 'r').read()
sub1 = 'AB'
sub2 = 'BA'


def find(array, index1=None, index2=None):
    try:
        if index1 is None and index2 is None:
            index1 = array.index(sub1)
            index2 = array.index(sub2)
        elif index1 is None:
            index1 = array.index(sub1, index2+2) + index2+2
        elif index2 is None:
            index2 = array.index(sub2, index1+2) + index1+2

        # if not overlapping, correct
        if abs(index1 - index2) > 1:
            return True
        # find other match for one of them
        if find(array, index2=index2) or find(array, index1=index1):
            return True
        else:
            return False

    # one of both not found
    except ValueError:
        return False


ans = find(string)
if ans is True:
    print("YES")
elif ans is False:
    print("NO")
