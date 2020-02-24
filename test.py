import numpy as np
import pandas as pd
import timeit

setup = """
import numpy as np
a = list(range(10000))
b = list(range(10000,20000))
np_a = np.arange(10000)
np_b = np.arange(10000,20000)
"""

statement_1 = "x, _ = zip(*zip(a, b))"
statement_2 = "x = [c for c, d in zip(a, b)]"
statement_3 = "c = np.vstack((np_a, np_b)); x = c[0, :]"

# print(timeit.timeit(statement_1, setup=setup, number=1000))
# print(timeit.timeit(statement_2, setup=setup, number=1000))
# print(timeit.timeit(statement_3, setup=setup, number=1000))

setup2 = """
l = list(range(100))
s = set(range(100))
l_used = list(range(30, 30000))
s_used = set(l_used)
"""

statement_4 = "x = len(l)"
statement_5 = "x = len(s)"

statement_6 = "[i for i in l if i not in l_used]"
statement_7 = "[i for i in s if i not in s_used]"
statement_8 = "[i for i in s - s_used]"

# print(timeit.timeit(statement_4, setup=setup2, number=100000))
# print(timeit.timeit(statement_5, setup=setup2, number=100000))

# print(pd.Series(timeit.repeat(statement_6, setup=setup2, number=1000, repeat=10)).describe())
# print(pd.Series(timeit.repeat(statement_7, setup=setup2, number=1000, repeat=10)).describe())
# print(pd.Series(timeit.repeat(statement_8, setup=setup2, number=1000, repeat=10)).describe())

setup3 = """
import numpy as np
scores = list(range(15000))
scores[7500] = 1e6
"""

statement_9 = "np_a = np.array(scores); max_index = np.argmax(np_a)"
statement_10 = "maxi = max(scores); max_index=scores.index(maxi)"
statement_11 = "max_index=scores.index(max(scores))"

# print(pd.Series(timeit.repeat(statement_9, setup=setup3, number=1000, repeat=10)).describe())
# print(pd.Series(timeit.repeat(statement_10, setup=setup3, number=1000, repeat=10)).describe())
# print(pd.Series(timeit.repeat(statement_11, setup=setup3, number=1000, repeat=10)).describe())


setup4 = """
large_set = set(range(30000))
small_set = set(range(30000, 30010))
"""

statement_12 = "large_set = large_set.union(small_set)"
statement_13 = "large_set.update(small_set)"

# print(pd.Series(timeit.repeat(statement_12, setup=setup4, number=1000, repeat=10)).describe())
# print(pd.Series(timeit.repeat(statement_13, setup=setup4, number=1000, repeat=10)).describe())


setup5 = """
from functools import reduce
import itertools
list_of_sets = [list(range(i, 10+i)) for i in range(8000)]
s = list()
"""

statement_14 = "s = set(itertools.chain.from_iterable(list_of_sets))"
statement_15 = "for x in list_of_sets: s.extend(x)"


# print(pd.Series(timeit.repeat(statement_14, setup=setup5, number=10, repeat=10)).describe())
# print(pd.Series(timeit.repeat(statement_15, setup=setup5, number=10, repeat=10)).describe())


setup6 = """
list_of_tuples = [(i, j) for i in range(100) for j in range(100, 200)]
second = lambda x: x[1]
"""

statement_16 = "[y for _, y in list_of_tuples]"
statement_17 = "list(map(second, list_of_tuples))"


print(pd.Series(timeit.repeat(statement_16, setup=setup6, number=1000, repeat=10)).describe())
print(pd.Series(timeit.repeat(statement_17, setup=setup6, number=1000, repeat=10)).describe())

