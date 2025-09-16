class Solution:
    def doesAliceWin(self, s: str) -> bool:
        """Alice only loses if there are zero vowels in s.
        If there is an odd number of vowels in s, then Alice removes the whole string, and wins.
        If there is an even number of vowels in s, then Alice removes a substring with an
            odd number of vowels, thereby leaving also an odd number of vowels.
            Bob might remove a substring with 0 vowels, and thereafter Alice removes the rest.
            Leaving no substring for Bob to remove, so Alice wins."""
        vowels = set(list("aeiou"))
        for char in s:
            if char in vowels:
                return True
        return False


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "TODO"
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
        funcs=["TODO"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
