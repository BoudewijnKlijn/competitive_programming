from collections import Counter
from typing import List


class Solution:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        """Words are all the same length. This is useful: we can step over s with word_length.
        Start from all possible remainders of len(s)%word_length.
        Every chunk from start:start+word_length should be a word. Count words seen so far.
        Left tracks from where count began.
        If not a word, then reset left and count to zero, since all words and only those words precisely
        must be in the substring.
        If too many of a single word, step the left pointer forward with word_length until count
        is less or equal again.
        Starting from each mod and stepping with word_length is essentially still only a single pass.
        """
        word_length = len(words[0])
        ans = list()
        needle = Counter(words)

        for mod in range(word_length):
            left = mod
            seen = Counter()
            for start_index in range(mod, len(s) - word_length + 1, word_length):
                substring = s[start_index : start_index + word_length]
                if substring not in needle:
                    # reset counter. set left to next possible starting point of permutation.
                    left = start_index + word_length
                    seen = Counter()
                    continue

                seen[substring] += 1
                while left < len(s) - 1 and any(seen[k] > v for k, v in needle.items()):
                    # remove word if too many compared with needle. step forward left until okay.
                    seen[s[left : left + word_length]] -= 1
                    left += word_length
                if needle == seen:
                    ans.append(left)
        return ans

    def too_slow(self, s: str, words: List[str]) -> List[int]:
        """Transform words to an integer. Less space to store.
        One pass over the string. At each position mark if the next word len characters form a word.
        Then another pass over the string.
        If begin of word, store in mod dict. Words have the same length, so every word length, check
        if another word begins. If not, remove from options. Otherwise keep checking
        If all words present, add begin idx to answer.
        Time Limit Exceeded
        179 / 182 testcases passed"""
        n = len(words)
        word_length = len(words[0])
        ans = list()

        unique_words = set(words)
        n_unique_words = len(unique_words)
        words_dict = dict(zip(unique_words, range(1, n_unique_words + 1)))
        needle = Counter(map(words_dict.get, words))

        word_begin = [None] * (len(s) - word_length + 1)
        for start_index in range(len(s) - word_length + 1):
            word = s[start_index : start_index + word_length]
            if word in words_dict:
                word_begin[start_index] = words_dict[word]

        if n == 1:
            # if only single word, we can create answer immediately.
            return [idx for idx, has_word in enumerate(word_begin) if has_word]

        # if more words
        mod_dict = {mod: [] for mod in range(word_length)}
        for idx, has_word in enumerate(word_begin):
            mod = idx % word_length
            if has_word is None:
                # remove all options. no word, so chain stops for this mod
                mod_dict[mod] = list()
                continue

            new_options = list()
            # if room to include all words, then add it to options
            if idx + word_length * n <= len(s):
                contains = Counter([has_word])
                new_options.append((idx, contains))
            for start_index, contains in mod_dict[mod]:
                # add word to existing ones
                contains[has_word] += 1
                if contains == needle:
                    # this was the last word to complete the permutation
                    ans.append(start_index)
                elif any(contains[k] > v for k, v in needle.items()):
                    # one of words in contains appears more than in needle. impossible.
                    continue
                else:
                    # add back to options
                    new_options.append((start_index, contains))
            mod_dict[mod] = new_options

        return ans


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "0030"
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
        funcs=["findSubstring"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
