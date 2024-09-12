class Solution:
    def minBitFlips(self, start: int, goal: int) -> int:
        # 1e9 has 32 digits (in binary)
        bin_start = bin(start)[2:].zfill(32)
        bin_goal = bin(goal)[2:].zfill(32)

        ans = 0
        for char1, char2 in zip(bin_start, bin_goal):
            if char1 != char2:
                ans += 1
        return ans
