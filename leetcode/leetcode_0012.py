

class Solution:
    def intToRoman(self, num: int) -> str:

        def convert(decimal, dec1, dec5, dec10):
            ans = ""
            if decimal == 9:
                ans += dec1 + dec10
                decimal = 0
            elif 5 <= decimal <= 8:
                ans += dec5
                decimal -= 5
            elif decimal == 4:
                ans += dec1 + dec5
                decimal = 0
            while decimal > 0:
                ans += dec1
                decimal -= 1
            return ans

        decimals = list(map(int, str(num).zfill(4)))
        ans = ""
        ans += convert(decimals[0], "M", "", "")
        ans += convert(decimals[1], "C", "D", "M")
        ans += convert(decimals[2], "X", "L", "C")
        ans += convert(decimals[3], "I", "V", "X")

        return ans


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "0012"
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
        funcs=["intToRoman"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
