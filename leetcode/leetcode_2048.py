import bisect
from collections import Counter


class Solution:
    """Precalculate balanced numbers."""

    def get_count(num):
        digits = list()
        while num > 0:
            num, mod = divmod(num, 10)
            digits.append(mod)
        return Counter(digits)

    def is_balanced(digits):
        for k, v in digits.items():
            if k != v:
                return False
        return True

    balanced_nums = [1]
    num = 2
    while balanced_nums[-1] <= 1_000_000:
        digits = get_count(num)
        if is_balanced(digits):
            balanced_nums.append(num)
        num += 1

    # balanced_nums = [
    #     1,
    #     22,
    #     122,
    #     212,
    #     221,
    #     333,
    #     1333,
    #     3133,
    #     3313,
    #     3331,
    #     4444,
    #     14444,
    #     22333,
    #     23233,
    #     23323,
    #     23332,
    #     32233,
    #     32323,
    #     32332,
    #     33223,
    #     33232,
    #     33322,
    #     41444,
    #     44144,
    #     44414,
    #     44441,
    #     55555,
    #     122333,
    #     123233,
    #     123323,
    #     123332,
    #     132233,
    #     132323,
    #     132332,
    #     133223,
    #     133232,
    #     133322,
    #     155555,
    #     212333,
    #     213233,
    #     213323,
    #     213332,
    #     221333,
    #     223133,
    #     223313,
    #     223331,
    #     224444,
    #     231233,
    #     231323,
    #     231332,
    #     232133,
    #     232313,
    #     232331,
    #     233123,
    #     233132,
    #     233213,
    #     233231,
    #     233312,
    #     233321,
    #     242444,
    #     244244,
    #     244424,
    #     244442,
    #     312233,
    #     312323,
    #     312332,
    #     313223,
    #     313232,
    #     313322,
    #     321233,
    #     321323,
    #     321332,
    #     322133,
    #     322313,
    #     322331,
    #     323123,
    #     323132,
    #     323213,
    #     323231,
    #     323312,
    #     323321,
    #     331223,
    #     331232,
    #     331322,
    #     332123,
    #     332132,
    #     332213,
    #     332231,
    #     332312,
    #     332321,
    #     333122,
    #     333212,
    #     333221,
    #     422444,
    #     424244,
    #     424424,
    #     424442,
    #     442244,
    #     442424,
    #     442442,
    #     444224,
    #     444242,
    #     444422,
    #     515555,
    #     551555,
    #     555155,
    #     555515,
    #     555551,
    #     666666,
    #     1224444,
    # ]

    def nextBeautifulNumber(self, n: int) -> int:
        """Precalculate all balanced numbers. Thereafter binary search."""
        idx = bisect.bisect_left(self.balanced_nums, n + 1)
        return self.balanced_nums[idx]


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "2048"
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
        funcs=["nextBeautifulNumber"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
