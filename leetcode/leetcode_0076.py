from collections import Counter


class Solution:
    def minWindow(self, s: str, t: str) -> str:
        """Loop over s until all characters of t are present (or more).
        Then increase left (to make window smaller) until one not present anymore.
        Keep track of counts with dict.
        Keep track of number of satisfied keys: faster then checking all keys.
            Only one key can change per iteration."""
        left = 0
        needles = Counter(t)
        n_keys = len(needles)
        counts = {k: 0 for k in needles.keys()}
        best = 0
        slice = tuple()
        n_satisfied = 0
        for right, char in enumerate(s):
            # no change if character not in t
            if char not in counts:
                continue
            counts[char] += 1
            # check if count is sufficient
            if counts[char] == needles[char]:
                n_satisfied += 1
            # decrease window size while all keys are satisfied
            while n_satisfied == n_keys:
                # update best window: left and right indices
                if not best or right - left + 1 < best:
                    slice = (left, right)
                    best = right - left + 1
                # reduce count of characters if removed
                if s[left] in counts:
                    counts[s[left]] -= 1
                    if counts[s[left]] == needles[s[left]] - 1:
                        n_satisfied -= 1
                left += 1
        return "" if not best else s[slice[0] : slice[1] + 1]


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "0076"
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
        funcs=["minWindow"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
