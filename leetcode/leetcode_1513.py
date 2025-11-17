from collections import defaultdict


class Solution:
    def numSub(self, s: str) -> int:
        """Do one pass to collect the longest substrings.
        Then decompose them into shorter and shorter ones.
        If length is k, then it can be decomposed it into k*(k+1)/2 parts.
        """
        MOD = 1_000_000_000 + 7
        lengths = defaultdict(int)
        length = 0
        for char in s:
            if char == "0":
                lengths[length] += 1
                length = 0
            else:
                length += 1
        lengths[length] += 1

        ans = 0
        for k, v in lengths.items():
            ans += v * k * (k + 1) // 2
        return ans % MOD


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "1513"
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
        funcs=["numSub"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
