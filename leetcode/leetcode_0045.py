from collections import deque
from typing import List


class Solution:
    def jump(self, nums: List[int]) -> int:
        return self.bfs(nums)

    def bfs(self, nums: List[int]) -> int:
        n = len(nums)
        data = deque([(0, 0)])  # n_jumps, index
        seen = set()
        while True:
            n_jumps, idx = data.popleft()
            if idx >= n - 1:
                return n_jumps
            max_jump = nums[idx]
            for jump_length in range(max_jump, 0, -1):
                new_idx = idx + jump_length
                if new_idx in seen:
                    # given we go from large to small jumps. if we have seen a larger index,
                    #   we must have seen the smaller indices as well.
                    break
                seen.add(new_idx)
                data.append((n_jumps + 1, new_idx))

    def dynamic_programming(self, nums: List[int]) -> int:
        """It is guaranteed that we can reach index n-1.
        We can take jumps in the range(1, j+1).
        Large jumps are not necessarily best, since we can skip other large jumps.
        Dynamic programming. Maintain list with the minimum amount of jumps to get to index.
        """
        n = len(nums)
        dp = [None] * n
        dp[0] = 0
        for i, max_jump in enumerate(nums):
            for jump_length in range(1, max_jump + 1):
                new_idx = i + jump_length
                if new_idx > n - 1:
                    continue
                if dp[new_idx] is None or dp[i] + 1 < dp[new_idx]:
                    dp[new_idx] = dp[i] + 1
        return dp[n - 1]


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=[
            "dynamic_programming",
            "bfs",
            # "dfs",
        ],
        data_file="leetcode_0045_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
