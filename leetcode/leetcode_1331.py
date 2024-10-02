from typing import List


class Solution:
    def arrayRankTransform(self, arr: List[int]) -> List[int]:
        unique = set(arr)
        rank = {val: rank for rank, val in enumerate(sorted(unique), start=1)}
        return [rank[val] for val in arr]
