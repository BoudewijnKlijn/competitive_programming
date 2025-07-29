from typing import List


class Solution:
    def smallestSubarrays(self, nums: List[int]) -> List[int]:
        return self.faster3(nums)

    def faster3(self, nums):
        """maintain minimum index for each bit of maximum bitwise or, from certain index

        Accepted
        59 / 59 testcases passed"""
        n = len(nums)

        ans = [1] * n
        max_bitwise_or = 0
        minimum_index_of_bit = dict()
        for i, num in enumerate(nums[::-1]):
            max_bitwise_or |= num
            bit = 1
            while bit <= max_bitwise_or:
                if (bit & max_bitwise_or) and (bit & num):
                    # (bit & xxx) returns 1 if bit is present in xxx
                    # update minimum index
                    minimum_index_of_bit[bit] = n - (i + 1)
                bit *= 2

            if minimum_index_of_bit:
                ans[n - i - 1] = max(minimum_index_of_bit.values()) - (n - (i + 1)) + 1

        return ans

    def faster2(self, nums):
        """Accepted
        59 / 59 testcases passed"""
        n = len(nums)

        # populate list with max bitwise OR from the back
        # (it can only increase by adding numbers)
        max_bitwise_or_list_reversed = list()
        max_bitwise_or = 0
        for num in nums[::-1]:
            max_bitwise_or |= num
            max_bitwise_or_list_reversed.append(max_bitwise_or)

        # maintain minimum index for each bit of maximum bitwise or, from certain index
        ans_reversed = list()
        minimum_index_of_bit = dict()
        for i, (num, max_bitwise_or) in enumerate(
            zip(nums[::-1], max_bitwise_or_list_reversed),
        ):
            bits_present = map(int, reversed(bin(max_bitwise_or)[2:]))
            bit = 1
            for bit_present in bits_present:
                # (bit & num) returns 1 if bit is present in num
                if bit_present and (bit & num):
                    # store index of current num
                    minimum_index_of_bit[bit] = n - (i + 1)
                bit *= 2

            if minimum_index_of_bit:
                ans = max(minimum_index_of_bit.values()) - (n - (i + 1)) + 1
            else:
                # only happens when max_bitwise_or == 0
                ans = 1
            ans_reversed.append(ans)

        return ans_reversed[::-1]

    def faster(self, nums):
        """Time Limit Exceeded
        58 / 59 testcases passed"""
        # populate list with max bitwise OR from the back
        # (it can only increase by adding numbers)
        max_bitwise_or_list_reversed = list()
        max_bitwise_or = 0
        for num in nums[::-1]:
            max_bitwise_or |= num
            max_bitwise_or_list_reversed.append(max_bitwise_or)

        # determine bitwise OR from index i. terminate when max reached.
        ans = list()
        prev_max_bitwise_or = None
        for i, max_bitwise_or in enumerate(max_bitwise_or_list_reversed[::-1]):
            # if no change in max bitwise or, then we know that the previously first number didn't
            # increase max bitwise or.
            # if both numbers are also the same, then we decrease ans by 1 (the previous start index)
            if max_bitwise_or == prev_max_bitwise_or and nums[i - 1] == nums[i]:
                ans.append(max(ans[-1] - 1, 1))
                # if previous ans is 1, it cannot become 0
            else:
                bitwise_or = 0
                for i2, num in enumerate(nums[i:], start=i):
                    bitwise_or |= num
                    if bitwise_or == max_bitwise_or:
                        ans.append(i2 - i + 1)
                        break

            prev_max_bitwise_or = max_bitwise_or
        return ans

    def too_slow(self, nums: List[int]) -> List[int]:
        """Time Limit Exceeded
        57 / 59 testcases passed"""
        # populate list with max bitwise OR from the back
        # (it can only increase by adding numbers)
        max_bitwise_or_list_reversed = list()
        max_bitwise_or = 0
        for num in nums[::-1]:
            max_bitwise_or |= num
            max_bitwise_or_list_reversed.append(max_bitwise_or)

        # determine bitwise OR from index i. terminate when max reached.
        ans = list()
        for i, max_bitwise_or in enumerate(max_bitwise_or_list_reversed[::-1]):
            bitwise_or = 0
            for i2, num in enumerate(nums[i:], start=i):
                bitwise_or |= num
                if bitwise_or == max_bitwise_or:
                    ans.append(i2 - i + 1)
                    break
        return ans


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=[
            # "smallestSubarrays",
            "faster3",
            "faster2",
            # "faster",
            #    "too_slow"
        ],
        data_file="leetcode_2411_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )

# +---------------------+------------+------------+
# |   smallestSubarrays |     faster |   too_slow |
# |---------------------+------------+------------|
# |            0.000032 |   0.000008 |   0.000005 |
# |            0.000006 |   0.000003 |   0.000002 |
# |            0.000013 |   0.000007 |   0.000005 |
# |            0.331204 |   0.025041 | 258.619297 |
# |            0.085396 | 271.949107 | 271.735084 |
# |            0.000011 |   0.000004 |   0.000002 |
# +---------------------+------------+------------+
# +-----------+-----------+
# |   faster3 |   faster2 |
# |-----------+-----------|
# |  0.000021 |  0.000018 |
# |  0.000004 |  0.000005 |
# |  0.000007 |  0.000013 |
# |  0.238358 |  0.327807 |
# |  0.053344 |  0.089991 |
# |  0.000007 |  0.000009 |
# +-----------+-----------+
