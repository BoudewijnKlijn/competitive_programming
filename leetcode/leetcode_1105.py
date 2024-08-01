from typing import List


class Solution:
    def minHeightShelves(self, books: List[List[int]], shelfWidth: int) -> int:
        dp = {}
        N = len(books)

        def height_dp(n_remaining):
            if n_remaining in dp:
                return dp[n_remaining]
            if n_remaining == 0:
                return 0

            sum_widths = 0
            heights = []
            for i, (w, h) in enumerate(books[N - n_remaining :], start=N - n_remaining):
                if sum_widths + w > shelfWidth:
                    break
                sum_widths += w
                heights.append(h)
                ans = max(heights) + height_dp(N - i - 1)
                dp[n_remaining] = min(dp.get(n_remaining, float("inf")), ans)

            return dp[n_remaining]

        height_dp(N)

        return dp[N]


s = Solution()
out = s.minHeightShelves(
    books=[[1, 1], [2, 3], [2, 3], [1, 1], [1, 1], [1, 1], [1, 2]], shelfWidth=4
)
print(out)  # 6

out = s.minHeightShelves(books=[[1, 3], [2, 4], [3, 2]], shelfWidth=6)
print(out)  # 4
