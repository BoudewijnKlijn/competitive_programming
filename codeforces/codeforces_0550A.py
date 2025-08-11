# string = open('in', 'r').read()
import os


def solve():
    string = input()
    sub1 = "AB"
    sub2 = "BA"

    def find(array, index1=None, index2=None):
        try:
            if index1 is None and index2 is None:
                index1 = array.index(sub1)
                index2 = array.index(sub2)
            elif index1 is None:
                index1 = array.index(sub1, index2 + 2) + index2 + 2
            elif index2 is None:
                index2 = array.index(sub2, index1 + 2) + index1 + 2
            if abs(index1 - index2) > 1:
                return True
            if find(array, index2=index2) or find(array, index1=index1):
                return True
            else:
                return False
        except ValueError:
            return False

    ans = find(string)
    if ans is True:
        print("YES")
    elif ans is False:
        print("NO")


if __name__ == "__main__":
    MULTIPLE_TESTS = False
    if not os.path.exists("LOCAL"):
        t = 1
        if MULTIPLE_TESTS:
            t = int(input())
        for _ in range(t):
            solve()
    else:
        import test_runner

        test_runner.main(solve, __file__, MULTIPLE_TESTS)
