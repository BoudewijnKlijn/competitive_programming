from typing import List


class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        n = len(haystack)
        m = len(needle)
        i = 0
        while i < n:
            j = 0
            while i + j < n and j < m:
                if haystack[i + j] == needle[j]:
                    j += 1
                else:
                    break
            if j == m:
                return i
            i += 1
        return -1
