from collections import Counter


class Solution:
    def equalFrequency(self, word: str) -> bool:
        count_letters = Counter(word)
        count_frequencies = Counter(count_letters.values())
        if (
            len(count_frequencies) == 2
            and max(count_frequencies.keys()) - 1 == min(count_frequencies.keys())
            and count_frequencies[max(count_frequencies.keys())] == 1
        ):
            return True
        elif (
            len(count_frequencies) == 2
            and min(count_frequencies.keys()) == 1
            and count_frequencies[min(count_frequencies.keys())] == 1
        ):
            return True
        elif len(count_frequencies) == 1 and list(count_frequencies.keys()) == [1]:
            return True
        elif len(count_letters) == 1 and len(word) > 1:
            return True
        return False


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["equalFrequency"],
        data_file="leetcode_2423_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
