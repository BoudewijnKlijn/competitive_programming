from typing import List


class Solution:
    def checkIfExist(self, arr: List[int]) -> bool:
        items = set()
        for n in arr:
            if n * 2 in items or n / 2 in items:
                return True
            items.add(n)
        return False
