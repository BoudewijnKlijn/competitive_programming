from typing import List


class Solution:
    def stoneGameII(self, piles: List[int]) -> int:
        """Dynamic programming with memoization."""
        N = len(piles)
        mem = {}

        def inner(used=0, M=1, alice_turn=True):
            if (used, M, alice_turn) in mem:
                return mem[(used, M, alice_turn)]

            if N - used <= M:
                if alice_turn:
                    ans = sum(piles[used:])
                else:
                    ans = 0
                mem[(used, M, alice_turn)] = ans
                return ans

            ans = 0 if alice_turn else float("inf")
            for x in range(1, 2 * M + 1):
                inner_result = inner(
                    used=used + x, M=max(M, x), alice_turn=not alice_turn
                )
                if alice_turn:
                    ans = max(ans, sum(piles[used : used + x]) + inner_result)
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
