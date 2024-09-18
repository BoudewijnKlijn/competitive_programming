from collections import Counter
from typing import List


class Solution:
    def uncommonFromSentences(self, s1: str, s2: str) -> List[str]:
        c1 = Counter(s1.split(" "))
        c2 = Counter(s2.split(" "))
        ans = list()
        for k1, v1 in c1.items():
            if v1 == 1 and k1 not in c2:
                ans.append(k1)
        for k2, v2 in c2.items():
            if v2 == 1 and k2 not in c1:
                ans.append(k2)
        return ans
