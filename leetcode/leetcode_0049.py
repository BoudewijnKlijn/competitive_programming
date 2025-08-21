from collections import defaultdict
from typing import List


class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        seen = defaultdict(list)
        for str in strs:
            sorted_str = "".join(sorted(str))
            seen[sorted_str].append(str)
        return list(seen.values())


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["groupAnagrams"],
        data_file="leetcode_0049_data.txt",
        exclude_data_lines=[0],
        check_result=True,
    )
