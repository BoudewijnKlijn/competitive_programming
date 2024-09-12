from typing import List


class Solution:
    def countConsistentStrings(self, allowed: str, words: List[str]) -> int:
        ans = 0
        for word in words:
            ans += all(c in allowed for c in word)
        return ans
