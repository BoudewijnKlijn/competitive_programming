from typing import List


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        """Simultaneously create hashmap and check if complement is present."""
        hashmap = dict()
        for i, num in enumerate(nums):
            complement = target - num
            if num in hashmap:
                # exactly one solution, so if already in hashmap, complement and num must be the same to be valid.
                if complement == num:
                    return [hashmap[num], i]
            else:
                hashmap[num] = i
                if complement in hashmap and complement != num:
                    return sorted([i, hashmap[target - num]])


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["twoSum"],
        data_file="leetcode_0001_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
