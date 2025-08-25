from typing import List


class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        n = len(strs)
        ans = ""
        for chars in zip(*strs):
            if len(chars) == n and len(set(chars)) == 1:
                ans += chars[0]
                continue
            break
        return ans
