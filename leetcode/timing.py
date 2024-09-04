import ast
import timeit
from functools import partial

import pandas as pd
from tabulate import tabulate


def time_and_result(func, *args):
    start_time = timeit.default_timer()
    result = func(*args)
    end_time = timeit.default_timer()
    return end_time - start_time, result


null = None


def timing(
    solution, funcs, data_file, exclude_data_lines=None, repeat=1, check_result=True
):
    print([x for x in dir(solution) if not x.startswith("__")])
    assert all(hasattr(solution, func) for func in funcs)

    with open(data_file, "r") as f:
        content = f.read().strip()

    all_runtimes = []
    for idx, data in enumerate(content.split("\n")):
        if exclude_data_lines and idx in exclude_data_lines:
            print(f"Skipped data line: {idx}")
            continue
        input_data, expected = data.split("->")
        expected = ast.literal_eval(expected.strip())
        args = ast.literal_eval(input_data.strip())
        runtimes = []
        for func in funcs:
            method = getattr(solution, func)
            if isinstance(args, tuple):
                runtime, result = time_and_result(method, *args)
            else:
                runtime, result = time_and_result(method, args)
            if check_result:
                assert expected == result, f"{expected} != {result}"
            if repeat > 1:
                if isinstance(args, tuple):
                    method_to_time = partial(method, *args)
                else:
                    method_to_time = partial(method, args)
                runtime = timeit.timeit(method_to_time, number=repeat)
            runtimes.append(runtime)

        all_runtimes.append(runtimes)

    print(
        tabulate(
            pd.DataFrame(data=all_runtimes, columns=funcs),
            headers="keys",
            tablefmt="psql",
            floatfmt=".6f",
            showindex=False,
        )
    )
