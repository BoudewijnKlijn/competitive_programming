from typing import List


class Solution:
    def hIndex(self, citations: List[int]) -> int:
        citations.sort()
        minimum = 1000
        best = 0
        for i, num in enumerate(citations[::-1], start=1):
            if num < minimum:
                minimum = num
            score = min(i, minimum)
            if score > best:
                best = score
            if num <= best:
                return best
        return best


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["hIndex"],
        data_file="leetcode_0274_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
