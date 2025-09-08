import os


def solve():
    """We get an array a, and we have to sort it, in minimal operations.
    f(b) can use two sort operations. Swap with max distance 2.
    g(b) can use one sort operation. Swap with max distance 1.
    Sub array is perfect if f(b) and g(b) are the same.

    If already sorted, then both are zero, and thus the same.
    Using the operations to sort seems too slow, because array is n elements long
        and with q queries, might need to sort it q times. Both 5e5.
    It may be so that if a subarray of the query is not perfect, then the query cannot be perfect
        either(?). If that is true (not sure though), the array to check is much smaller,
        and can be reused: DP.

    My idea, but not going to implement it:
        - apply the queries in some order. Smaller ones before longer ones
        - store results
        - if small queries not perfect, than longer encompassing longer query also not
        - this would be more efficient, because reusing smaller queries
        - if small query is perfect, then still need to check longer query. maybe possible to
            store sorted result??

    """
    n, q = list(map(int, input().split()))
    a = list(map(int, input().split()))
    for _ in range(q):
        # get query
        left, right = list(map(int, input().split()))

        # if sorted, both zero, so YES
        # TODO: this may be slow !! sorting q times and arrow of length n
        if sorted(a[left - 1 : right]) == a[left - 1 : right]:
            print("YES")
            continue
        # TODO
        # print("NO")


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
