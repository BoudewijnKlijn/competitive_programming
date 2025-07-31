from typing import List


class Solution:
    def subarrayBitwiseORs(self, arr: List[int]) -> int:
        return self.simplify_then_brute_force_with_stop(arr)

    def simplify2(self, arr: List[int]) -> int:
        """simplify with pointers. less space but slower"""
        n = len(arr)
        read_pointer, write_pointer = 1, 1
        while read_pointer < n:
            if arr[read_pointer] != arr[write_pointer - 1]:
                arr[write_pointer] = arr[read_pointer]
                write_pointer += 1
            read_pointer += 1
        return self.brute_force_with_stop(arr[:write_pointer])

    def simplify_then_brute_force_with_stop(self, arr: List[int]) -> int:
        """Remove numbers if they are equal to previous number.
        Accepted
        85 / 85 testcases passed"""
        new_arr = list()
        prev = None
        for num in arr:
            if num == prev:
                continue
            new_arr.append(num)
            prev = num
        return self.brute_force_with_stop(new_arr)

    def brute_force_with_stop(self, arr: List[int]) -> int:
        """Try all subarrays, unless no more bits are added in the remaining indices.
        Time Limit Exceeded
        83 / 85 testcases passed"""
        n = len(arr)

        # max OR from right to left (used later to determine bits added by remaining indices)
        max_bitwise_or_right_to_left = list()
        bitwise_or = 0
        for num in arr[::-1]:
            bitwise_or |= num
            max_bitwise_or_right_to_left.append(bitwise_or)
        distinct = set(max_bitwise_or_right_to_left)

        for i, num in enumerate(arr):
            bitwise_or = num
            distinct.add(bitwise_or)
            for j, n_extra in enumerate(arr[i + 1 :], start=i + 1):
                bitwise_or |= n_extra
                distinct.add(bitwise_or)

                # stop when no more bits are added by remaining numbers.
                if (
                    bitwise_or & max_bitwise_or_right_to_left[n - 2 - j]
                    == max_bitwise_or_right_to_left[n - 2 - j]
                ):
                    break

        return len(distinct)

    def brute_force(self, arr: List[int]) -> int:
        """Try all subarrays.

        Time Limit Exceeded
        77 / 85 testcases passed"""
        distinct = set()
        for i, num in enumerate(arr):
            bitwise_or = num
            distinct.add(bitwise_or)
            for n_extra in arr[i + 1 :]:
                bitwise_or |= n_extra
                distinct.add(bitwise_or)

        return len(distinct)


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=[
            # "subarrayBitwiseORs",
            # "brute_force",
            # "brute_force_with_stop",
            "simplify_then_brute_force_with_stop",
            "simplify2",
        ],
        data_file="leetcode_0898_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
