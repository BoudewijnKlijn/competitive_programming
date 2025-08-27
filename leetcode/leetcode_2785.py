from itertools import chain


class Solution:
    def sortVowels(self, s: str) -> str:
        vowel_indices = list()
        vowels = {k: 0 for k in sorted("AEIOUaeiou")}
        for i, char in enumerate(s):
            if char in vowels:
                vowels[char] += 1
                vowel_indices.append(i)

        s_list = list(s)
        for idx, replacement in zip(
            vowel_indices, chain.from_iterable((k * v for k, v in vowels.items()))
        ):
            s_list[idx] = replacement
        return "".join(s_list)


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["sortVowels"],
        data_file="leetcode_2785_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
