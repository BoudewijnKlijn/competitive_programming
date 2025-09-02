from collections import deque


class Solution:
    def simplifyPath(self, path: str) -> str:
        # combine subsequent slashes into one slash
        n = len(path)
        path = list(path)
        write_pointer = 1
        prev = path[0]
        for i in range(1, n):
            char = path[i]
            if char == "/" and char == prev:
                prev = char
                continue
            path[write_pointer] = path[i]
            write_pointer += 1
            prev = char
        path = "".join(path[:write_pointer])

        # split path into folders. add folders to new_path
        queue = deque(path.split("/"))
        new_path = list()
        while queue:
            item = queue.popleft()
            # if empty. do nothing
            if not item:
                continue
            # go one folder up. remove last folder in new path.
            elif item == "..":
                try:
                    new_path.pop()
                # if nothing to pop. do nothing
                except IndexError:
                    continue
            # go to this directory. do nothing
            elif item == ".":
                continue
            else:
                new_path.append(item)
        # produce final output. start with slash and separate with slash.
        return "/" + "/".join(new_path)


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "0071"
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
        funcs=["simplifyPath"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
