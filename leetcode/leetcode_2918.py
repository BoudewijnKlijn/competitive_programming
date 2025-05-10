from typing import List


class Solution:
    def minSum(self, nums1: List[int], nums2: List[int]) -> int:
        """Only allowed to replace 0's with positive integers.
        If one array has no zeros, and has a lower sum than the other, it is impossible.
        Otherwise, replace all zeros with ones in both.
        If not equal, increase integers in the lower one until same sum.
        Cannot decrease integers in higher sum array, as that would make zeros or negative integers.
        """
        sum1 = sum(nums1)
        sum2 = sum(nums2)
        n_zeros1 = nums1.count(0)
        n_zeros2 = nums2.count(0)
        if n_zeros1 == 0 and sum1 < sum2 + n_zeros2:
            return -1
        if n_zeros2 == 0 and sum2 < sum1 + n_zeros1:
            return -1
        return max(sum1 + n_zeros1, sum2 + n_zeros2)


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["minSum"],
        data_file="leetcode_2918_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
