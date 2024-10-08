class Solution:
    def minSwaps(self, s: str) -> int:
        """We always have to swap different symbols, otherwise not helpful.
        The balanced string always starts with [ and ends with ].
        [ can be seen as +1 and ] as -1.
        From left to right, whenever we dip below zero, the string is not balanced
        and we need to swap characters.
        (or from right to left, we should not go above zero.)
        We can use two pointers, one from the start and one from the end.
        Move the pointers until a wrong character is found on both ends and swap them.
        """
        if len(s) == 0:
            return 0

        # s = list(s)  # its not needed to really swap. saves time to skip swapping.
        char_value = {"[": 1, "]": -1}
        left, right = 0, len(s) - 1
        left_sum, right_sum = 0, 0
        swaps = 0
        while left <= right:
            while left <= right and left_sum >= 0:
                left_char = s[left]
                left_sum += char_value[left_char]
                left += 1
            while left <= right and right_sum <= 0:
                right_char = s[right]
                right_sum += char_value[right_char]
                right -= 1

            if left_sum < 0 and right_sum > 0:
                # swap left and right. (pointers are one spot further)
                # its not needed to really swap. saves time to skip swapping.
                # s[left - 1], s[right + 1] = s[right + 1], s[left - 1]
                left_sum, right_sum = 1, -1
                swaps += 1
        return swaps


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["minSwaps"],
        data_file="leetcode_1963_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
