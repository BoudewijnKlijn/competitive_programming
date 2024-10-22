class Solution:
    def maxUniqueSplit(self, s: str) -> int:
        # start with first char as single substring
        # create new substrings by concatenating new char to last substring,
        #  or by appending new char as extra substring
        # repeat for all chars
        collection = [(s[0],)]
        for char in s[1:]:
            new = list()
            for substrings in collection:
                # concatenate
                new.append(substrings[:-1] + (substrings[-1] + char,))
                # append
                new.append(substrings + (char,))
                # removing duplicates here fails the fourth testcase
            collection = new
        # make unique and return len
        return max(map(len, map(set, collection)))


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["maxUniqueSplit"],
        data_file="leetcode_1593_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
