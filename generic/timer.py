import os
import time
import timeit
from operator import attrgetter

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def compare(funcs, base_name, number=100, repeat=1_000, validate=True):
    if validate:
        results = []
        for func in funcs:
            results.append(func())
        assert all(r == results[0] for r in results), "Results must be equal."

    results = list()
    for i, func in enumerate(funcs):
        print(i, end="...")
        result = timeit.Timer(func).repeat(repeat, number=number)
        results.append(result)
    print()

    df = pd.DataFrame(data=zip(*results), columns=map(attrgetter("__name__"), funcs))

    # timestamp = str(time.time()).replace(".", "_")
    file_name = os.path.join(
        os.path.dirname(__file__), base_name.replace(".py", "_")  # + timestamp
    )

    plot_timings(df, file_name)


def plot_timings(df, file_name):
    plt.suptitle("Relative to lowest mean")
    medians = df.mean()
    best_median = medians.min()
    df2 = df / best_median
    sns.kdeplot(df2, common_norm=False, bw_adjust=1.5)

    print(f"Raw medians:\n{medians}")
    print(f"\nScaled medians (relative to best):\n{df2.median()}")

    plt.tight_layout()
    plt.savefig(file_name)
    plt.close()
