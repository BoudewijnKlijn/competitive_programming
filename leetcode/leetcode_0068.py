from typing import List


class Solution:
    def fullJustify(self, words: List[str], maxWidth: int) -> List[str]:
        def justify(line, last_line=False):
            n_words_in_line = len(line)
            if n_words_in_line == 1 or last_line:
                out = " ".join(line)
                out += (maxWidth - len(out)) * " "
            else:
                n_spaces = maxWidth - sum(map(len, current_line))
                # each word gets at least div, and the first mod get 1 extra.
                div, mod = divmod(n_spaces, n_words_in_line - 1)
                out = ""
                for i, word in enumerate(line[:-1]):
                    out += word + " " * div
                    if i < mod:
                        out += " "
                out += line[-1]
            return out

        lines = [[]]
        ans = list()
        for word in words:
            current_line = lines[-1]
            n_words_in_line = len(current_line)
            if n_words_in_line + sum(map(len, current_line)) + len(word) <= maxWidth:
                # enough space to add the word.
                lines[-1].append(word)
            else:
                # not enough space. justify current line and thereafter create new line.
                ans.append(justify(current_line))
                lines.append([word])

        ans.append(justify(lines[-1], last_line=True))
        return ans


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "0068"
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
        funcs=["fullJustify"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
