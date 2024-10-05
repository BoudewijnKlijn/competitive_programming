from collections import Counter


class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        """Hashmap + sliding window
        Start with piece of s2 that has length of s1.
        Create Counter and check for equality
        If not the same, iteratively add and remove a character and change count
        If never the same, return False."""
        c1 = Counter(s1)
        c2 = Counter(s2[: len(s1)])
        if c1 == c2:
            return True
        for char_remove, char_add in zip(s2, s2[len(s1) :]):
            c2[char_remove] -= 1
            if char_add in c2:
                c2[char_add] += 1
            else:
                c2[char_add] = 1
            if c1 == c2:
                return True

        return False
