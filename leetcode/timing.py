import timeit
from functools import partial

import pandas as pd
from tabulate import tabulate


def timing(data_file, funcs, args_idx, solution):
    print([x for x in dir(solution) if not x.startswith("__")])
    assert all(hasattr(solution, func) for func in funcs)

    with open(data_file, "r") as f:
        content = f.read().strip()

    all_runtimes = []
    for idx, data in enumerate(content.split("\n")):
        if idx not in args_idx:
            print(f"skipped data {idx}")
            continue
        args = eval(data)
        runtimes = []
        answers = []
        for func in funcs:
            method = getattr(solution, func)
            method_to_time = partial(method, args)
            runtime = timeit.timeit(method_to_time, number=1)
            runtimes.append(runtime)

            if runtime < 1:
                ans = method_to_time()
                answers.append(ans)
                print(answers)
                # assert all(ans == answers[0] for ans in answers)

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
