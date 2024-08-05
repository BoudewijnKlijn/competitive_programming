from collections import Counter
from typing import List


class Solution:
    def kthDistinct(self, arr: List[str], k: int) -> str:
        c = Counter(arr)
        for key, value in c.items():
            if value == 1:
                k -= 1
                if not k:
                    return key
        return ""
