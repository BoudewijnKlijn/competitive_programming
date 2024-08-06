from collections import Counter
from typing import List


class Solution:
    def minimumPushes(self, word: str) -> int:
        c = Counter(word)

        ans = 0
        mult = 1
        i = 0
        for i, (_, v) in enumerate(c.most_common()):
            ans += v * mult
            i += 1
            if i % 8 == 0:
                mult += 1
                i = 0
        return ans
