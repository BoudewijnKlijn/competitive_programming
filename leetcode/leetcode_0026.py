from typing import List


class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        unique = set()
        write_idx = 0
        for num in nums:
            if num in unique:
                continue
            unique.add(num)
            nums[write_idx] = num
            write_idx += 1
        return write_idx


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["TODO"],
        data_file="leetcode_XXXX_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
