from collections import Counter


class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        """Ransomnote can be constructed if all letters appear at least as often in magazine."""
        count_ransom = Counter(ransomNote)
        count_magazine = Counter(magazine)
        for letter, count in count_ransom.items():
            if count_magazine[letter] < count:
                return False
        return True


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "0383"
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
        funcs=["canConstruct"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
