from typing import List


class Solution:
    def isOneBitCharacter(self, bits: List[int]) -> bool:
        """If last character is a one, it must be two-bit.
        If last character is zero, it may be one bit or two bit.
            If number of ones before the last character is even, last char must be one bit, so, True.
            Otherwise False
        """
        if bits[-1] == 1:
            return False

        # count number of ones before the last position
        count = 0
        for char in bits[-2::-1]:
            if char == 0:
                break
            count += 1

        # if number of ones is even, last bit must be single bit, so True, otherwise False
        if count % 2 == 0:
            return True
        return False


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "0717"
    data_file = os.path.join(os.path.dirname(__file__), f"leetcode_{PROBLEM}_data.txt")

    # # generate testcases
    # import sys

    # sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    # from generic.helper import InputInteger, InputList, generate_testcases

    # arr1 = InputList(n_min_max=(2, 100_000), val_min_max=(0, 10_000))
    # int1 = InputInteger(val_min_max=(0, 10_000))
    # vars = generate_testcases(structure=(arr1,), n=1, data_file=data_file, solver=None)

    timing(
        solution=Solution(),
        funcs=["isOneBitCharacter"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
