import os


def solve():
    """Its easier to think about this in binary.
    When we divide by half, we bitshift right once. The resulting number is added to the other.
    From lowest bits, if bits overlap then carry one bit to the next higher bit.
    We can do at most k operations. Thereafter the lowest bit becomes 1 with both users, and
    neither can be divided anymore.
    It can be visualized as a tree.
        Root is 2**(k+1). 1000...
        Then left and right are both 2**k.  0100...
        Then left left is 2**(k-1) 0010... and left right is 0110...
        Too many leaf nodes: 2**60, so how do I know which route to take...
    Maybe easier to start at the leaf node. Multiply with 2. Have to undo the lowest bit.
    One of them is always more than half, so that one cannot be multiplied with 2.

    """
    k, x = list(map(int, input().split()))

    if x == 1 << k:
        print(0)
        print()
        return

    comp = (1 << (k + 1)) - x

    ans = list()
    while x != (1 << k):
        # multiply the smaller one with two
        if x < comp:
            ans.append(1)
            new = x << 1
            diff = new - x
            comp -= diff
            x = new
        else:
            ans.append(2)
            new = comp << 1
            diff = new - comp
            x -= diff
            comp = new

    print(len(ans))
    print(*reversed(ans))


if __name__ == "__main__":
    MULTIPLE_TESTS = True

    if not os.path.exists(os.path.join("codeforces", "LOCAL")):
        t = 1
        if MULTIPLE_TESTS:
            t = int(input())

        for _ in range(t):
            solve()
    else:
        import test_runner

        test_runner.main(solve, __file__, MULTIPLE_TESTS)
