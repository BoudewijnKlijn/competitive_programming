import timeit
from functools import partial

import pandas as pd
from tabulate import tabulate


def time_and_result(func, *args, **kwargs):
    start_time = timeit.default_timer()
    result = func(*args, **kwargs)
    end_time = timeit.default_timer()
    return end_time - start_time, result


def timing(solution, funcs, data_file, data_lines=None, repeat=1):
    print([x for x in dir(solution) if not x.startswith("__")])
    assert all(hasattr(solution, func) for func in funcs)

    with open(data_file, "r") as f:
        content = f.read().strip()

    all_runtimes = []
    for idx, data in enumerate(content.split("\n")):
        if data_lines and idx not in data_lines:
            print(f"Skipped data line: {idx}")
            continue
        input_data, expected = data.split("->")
        expected = eval(expected.strip())
        args = eval(input_data.strip())
        runtimes = []
        for func in funcs:
            method = getattr(solution, func)
            if repeat > 1:
                method_to_time = partial(method, args)
                runtime = timeit.timeit(method_to_time, number=repeat)
                runtimes.append(runtime)
                continue
            runtime, result = time_and_result(method, args)
            runtimes.append(runtime)
            assert expected == result, f"{expected} != {result}"

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
