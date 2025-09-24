class Solution:
    def fractionToDecimal(self, numerator: int, denominator: int) -> str:
        if numerator == 0:
            return "0"

        ans = ""
        if numerator * denominator < 0:
            ans += "-"
        numerator = abs(numerator)
        denominator = abs(denominator)

        seen = dict()
        added_period = False
        while numerator != 0:
            if numerator in seen:
                idx = seen[numerator]
                ans = ans[:idx] + "(" + ans[idx:] + ")"
                break

            if added_period:
                # only store after period is added
                seen[numerator] = len(ans)
            div, numerator = divmod(numerator, denominator)
            numerator *= 10
            ans += str(div)

            # add . only once, if numerator not zero after first division
            if not added_period and numerator != 0:
                ans += "."
                added_period = True

        return ans


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "0166"
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
        funcs=["fractionToDecimal"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
