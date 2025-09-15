class Solution:
    def canBeTypedWords(self, text: str, brokenLetters: str) -> int:
        words = text.split()
        brokenLetters = set(list(brokenLetters))
        ans = 0
        for word in words:
            for char in word:
                if char in brokenLetters:
                    break
            else:
                ans += 1
        return ans


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "1935"
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
        funcs=["canBeTypedWords"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
