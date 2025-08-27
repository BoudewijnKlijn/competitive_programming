

class Solution:
    def findTheLongestSubstring(self, s: str) -> int:
        # brute force with slight optimization

        vowels = "aeuio"
        N = len(s) + 1
        prefix_sums = [[0 for _ in range(N)] for _ in range(len(vowels))]
        vowels_dict = {char: i for i, char in enumerate(vowels)}

        # 1-indexed
        for i, char in enumerate(s, start=1):
            for vowel in vowels_dict:
                # vowel: increase prefix by 1
                if vowel == char:
                    prefix_sums[vowels_dict[vowel]][i] = (
                        1 + prefix_sums[vowels_dict[vowel]][i - 1]
                    )

                # no vowel: keep the same
                else:
                    prefix_sums[vowels_dict[vowel]][i] = prefix_sums[
                        vowels_dict[vowel]
                    ][i - 1]

        # try all start and end positions: 1/2 * n * (n+1)
        # if one vowel count is odd, go to next
        # only check options which are longer than longest
        longest = 0
        for start in range(1, N):
            for end in range(start + longest, N):
                correct = True
                for vowel in vowels:
                    count = (
                        prefix_sums[vowels_dict[vowel]][end]
                        - prefix_sums[vowels_dict[vowel]][start - 1]
                    )
                    if count % 2 == 1:
                        correct = False
                        break
                if correct:
                    length = end - start + 1
                    if length > longest:
                        longest = length
        return longest


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["findTheLongestSubstring"],
        data_file="leetcode_1371_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
