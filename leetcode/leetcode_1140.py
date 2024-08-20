from typing import List


class Solution:
    def stoneGameII(self, piles: List[int]) -> int:
        """Recursion with memoization.
        Suffix sum optimization idea from editorial."""
        N = len(piles)
        mem = {}
        suffix_sum = [sum(piles)]
        for stones in piles:
            suffix_sum.append(suffix_sum[-1] - stones)

        def inner(used=0, M=1, alice_turn=True):
            if (used, M, alice_turn) in mem:
                return mem[(used, M, alice_turn)]

            if N - used <= M:
                if alice_turn:
                    ans = suffix_sum[used]
                else:
                    ans = 0
                mem[(used, M, alice_turn)] = ans
                return ans

            ans = 0 if alice_turn else float("inf")
            for x in range(1, 2 * M + 1):

                if used + x > N:
                    # early stopping and prevent index error
                    break

                inner_result = inner(
                    used=used + x, M=max(M, x), alice_turn=not alice_turn
                )
                if alice_turn:
                    ans = max(
                        ans, suffix_sum[used] - suffix_sum[used + x] + inner_result
                    )
                else:
                    ans = min(ans, inner_result)

            mem[(used, M, alice_turn)] = ans
            return ans

        return inner()


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["stoneGameII"],
        data_file="leetcode_1140_data.txt",
        data_lines=[0, 1, 2],
    )
