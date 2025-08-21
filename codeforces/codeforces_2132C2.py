import os

# number_and_coins = {3**x: int(3 ** (x + 1) + x * 3 ** (x - 1)) for x in range(20)}
# for n, cost in number_and_coins.items():
#     avg_price = cost / n
#     print(avg_price)


def get_coins(x):
    return int(3 ** (x + 1) + x * 3 ** (x - 1))


def solve():
    """The avg price per watermelon increases with 0.33. Always better to buy in smaller quantities.
    Limitation is k (maximum number of deals).
    If place for two more deals, then split larger deal up in three smaller deals, and pay less.
    First determine if possible within k, then adjust to smaller quantities."""
    n, k = list(map(int, input().split()))

    # greedy
    x = 20
    deals_of_x = dict()
    n_deals = 0
    while n > 0:
        while 3**x > n:
            x -= 1
        n -= 3**x
        n_deals += 1
        if x in deals_of_x:
            deals_of_x[x] += 1
        else:
            deals_of_x[x] = 1

    if n_deals > k:
        # not possible, not even if bought in largest quantities
        print(-1)
        return

    # possible. now optimize further.
    k -= n_deals
    while k >= 2:
        max_reductions = k // 2
        # split one large deal into three smaller deals
        largest_deal_x = max(deals_of_x)
        if largest_deal_x == 0:
            break

        smaller_deal_x = largest_deal_x - 1
        largest_deal_count = deals_of_x[largest_deal_x]

        change = min(largest_deal_count, max_reductions)
        deals_of_x[largest_deal_x] -= change
        if deals_of_x[largest_deal_x] == 0:
            del deals_of_x[largest_deal_x]
        if smaller_deal_x in deals_of_x:
            deals_of_x[smaller_deal_x] += 3 * change
        else:
            deals_of_x[smaller_deal_x] = 3 * change
        k -= 2 * change

    ans = sum(get_coins(x) * count for x, count in deals_of_x.items())
    print(ans)


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
