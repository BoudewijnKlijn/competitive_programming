import os
from collections import Counter, defaultdict


def solve():
    """Its possible if counts correspond with keys and sum of counts equals n or k%v==0."""
    n = int(input())
    b = list(map(int, input().split()))
    counts = Counter(b)
    for k, v in counts.items():
        div, mod = divmod(v, k)
        if v < k or mod != 0:
            print(-1)
            return

    if sum(counts.values()) != n:
        print(-1)
        return

    # possible, i think
    # get all values the correct number of times and store at correct k.
    # might be a mix of multiple numbers, therefore list
    values = defaultdict(list)
    val = 1
    for k, v in counts.items():
        vv = v
        while vv > 0:
            values[k].extend([val] * k)
            vv -= k
            val += 1

    # use mapping to construct output. pop from values
    ans = list()
    for bb in b:
        ans.append(values[bb].pop())
    print(*ans)


if __name__ == "__main__":
    MULTIPLE_TESTS = True

    if not os.path.exists("LOCAL"):
        t = 1
        if MULTIPLE_TESTS:
            t = int(input())

        for _ in range(t):
            solve()
    else:
        import test_runner

        test_runner.main(solve, __file__, MULTIPLE_TESTS)
