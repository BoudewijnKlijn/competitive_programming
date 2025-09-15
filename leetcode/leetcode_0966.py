from typing import List


class Solution:
    def spellchecker(self, wordlist: List[str], queries: List[str]) -> List[str]:
        word_set = set(wordlist)

        lowercase_dict = dict()
        for word in wordlist:
            if word.lower() not in lowercase_dict:
                lowercase_dict[word.lower()] = word

        def replace_vowels(word):
            tmp = ""
            for char in word:
                if char.lower() in vowels:
                    tmp += "_"
                else:
                    tmp += char.lower()
            return tmp

        vowel_dict = dict()
        vowels = set(list("aeiou"))
        for word in wordlist:
            tmp = replace_vowels(word)
            if tmp not in vowel_dict:
                vowel_dict[tmp] = word

        ans = list()
        for query in queries:
            # exact match
            if query in word_set:
                ans.append(query)
                continue

            # match except case
            query_lower = query.lower()
            if query_lower in lowercase_dict:
                ans.append(lowercase_dict[query_lower])
                continue

            # match except vowels
            query_vowel = replace_vowels(query)
            if query_vowel in vowel_dict:
                ans.append(vowel_dict[query_vowel])
                continue

            ans.append("")
        return ans


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "0966"
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
        funcs=["spellchecker"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
