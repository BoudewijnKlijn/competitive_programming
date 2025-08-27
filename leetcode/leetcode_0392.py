

class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        if not s:
            return True
        found = 0
        n = len(s)
        for char in t:
            if s[found] == char:
                found += 1
                if found == n:
                    return True
        return False
