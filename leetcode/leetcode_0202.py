class Solution:
    def isHappy(self, n: int) -> bool:
        """Faster than the string method (although leetcode thinks the opposite)."""
        seen = set()
        while True:
            total = 0
            if n == 1:
                return True
            elif n in seen:
                return False
            seen.add(n)
            while n > 0:
                n, mod = divmod(n, 10)
                total += mod**2
            n = total

    def using_string(self, n: int) -> bool:
        seen = set()
        while True:
            if n == 1:
                return True
            elif n in seen:
                return False
            seen.add(n)
            total = 0
            for x in str(n):
                total += int(x) ** 2
            n = total


# +-----------+----------------+
# |   isHappy |   using_string |
# |-----------+----------------|
# |  0.001067 |       0.001662 |
# |  0.003315 |       0.004966 |
# |  0.003405 |       0.005019 |
# |  0.004320 |       0.006504 |
# |  0.003337 |       0.004976 |
# |  0.002281 |       0.003300 |
# |  0.004467 |       0.006722 |
# |  0.002090 |       0.003086 |
# |  0.004169 |       0.006386 |
# |  0.003476 |       0.005123 |
# |  0.004705 |       0.007129 |
# +-----------+----------------+


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "0202"
    data_file = os.path.join(os.path.dirname(__file__), f"leetcode_{PROBLEM}_data.txt")

    # # generate testcases
    # import sys

    # sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    # from generic.helper import InputInteger, generate_testcases

    # int1 = InputInteger(val_min_max=(0, 2**30))
    # vars = generate_testcases(
    #     structure=(int1,), n=10, data_file=data_file, solver=Solution().isHappy
    # )

    timing(
        solution=Solution(),
        funcs=["isHappy", "using_string"],
        data_file=data_file,
        exclude_data_lines=None,
        repeat=1000,
        check_result=True,
    )
