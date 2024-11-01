class Solution:
    def makeFancyString(self, s: str) -> str:
        ans = ""
        for char in s:
            if len(ans) < 2 or char != ans[-1] or char != ans[-2]:
                ans += char
        return ans
