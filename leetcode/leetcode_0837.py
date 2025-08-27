

class Solution:
    def new21Game(self, n: int, k: int, maxPts: int) -> float:
        """Alice starts with zero points.
        Alice draws integer between 1-maxPts(inclusive), with equal proability: 1/maxPts.
        Alice stops drawing integers when total points is >= k.
        What is probability points <= n?
        The moment before final draw, points is at least max(0, k+1-maxPts),
            and at most max(0, k-1).
        If k = 0, game stops immediately. ans = 1 if n > 0.
        If k = 1, game stops after 1 draw. ans = 1 if n > maxPts else n/maxPts.
        If k = 2, game stops after 1 or 2 draws (first draw must be 1).
            After first draw, points are 2 to maxPts, each with probability 1/maxPts
            After second draw, 2 to maxPts+1 get an additional 1/(maxPts**2).
                P[2 to maxPts] = 1/maxPts + 1/(maxPts**2), and P[maxPts + 1] = 1/(maxPts**2)
        Could continue. Since we draw at least 1, there are at most k draws.
        Values higher than n dont matter.
        """
        return self.window(n, k, maxPts)

    def window(self, n: int, k: int, maxPts: int) -> float:
        """Use sliding window to prevent recalculating the prob of being at smaller numbers."""
        if k == 0:
            return 1

        prob = [1] + [0] * n
        window_sum = prob[0]
        for idx in range(1, n + 1):
            prob[idx] = window_sum / maxPts
            if idx < k:
                # increase window if still possible to draw integers
                window_sum += prob[idx]
            if idx - maxPts >= 0:
                # decrease window if even if maxPts is drawn it is too little
                window_sum -= prob[idx - maxPts]
            if idx >= k + maxPts:
                # impossible to go to this index. max = k - 1 + maxPts.
                break

        return round(sum(prob[k : n + 1]), 5)

    def recursion(self, n: int, k: int, maxPts: int) -> float:
        """Prob of being at a number is prob from being at smaller number and then drawing
            the precise difference. Prob of drawing each number is equal. Prob of being at
            smaller number can be calculated using recursion.
        Use base cases P[0] = 1 and P[<0] = 0
        Starting at n results in recursion error. Starting from small numbers is fine, but slow still.
        Time complexity ~O(n*maxPts)

        Time Limit Exceeded
        96 / 151 testcases passed
        """
        if k == 0:
            return 1

        memo = {0: 1}

        def prob(points):
            if points not in memo:
                memo[points] = (
                    sum(
                        prob(points - draw_integer)
                        for draw_integer in range(1, maxPts + 1)
                        if 0 <= points - draw_integer < k
                    )
                    / maxPts
                )

            return memo[points]

        # populate memo from small numbers to prevent recursionerror
        for points in range(n + 1):
            prob(points)

        ans = round(
            sum(prob(points) for points in range(max(1, k), n + 1)),
            5,
        )
        return ans

    def bruteforce(self, n: int, k: int, maxPts: int) -> float:
        """Complexity is O(n*k), worst case 10**8.
        Time Limit Exceeded
        97 / 151 testcases passed"""
        add_prob = 1 / maxPts
        prob = [1] + [0] * n
        for draw in range(k):
            idx = draw + 1
            add = prob[draw] * add_prob
            while idx < n + 1 and idx <= draw + maxPts:
                prob[idx] += add
                idx += 1
            prob[draw] = 0
        return round(sum(prob[: n + 1]), 5)


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["bruteforce", "recursion", "window"],
        data_file="leetcode_0837_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )

# +--------------+-------------+----------+
# |   bruteforce |   recursion |   window |
# |--------------+-------------+----------|
# |     0.000011 |    0.000022 | 0.000005 |
# |     0.000004 |    0.000011 | 0.000003 |
# |     0.000005 |    0.000018 | 0.000004 |
# |     0.000009 |    0.000020 | 0.000004 |
# |     0.000017 |    0.000044 | 0.000005 |
# |     0.957595 |    1.835523 | 0.001426 |
# |     1.542043 |    4.301784 | 0.000735 |
# |     0.000006 |    0.000023 | 0.000004 |
# +--------------+-------------+----------+
