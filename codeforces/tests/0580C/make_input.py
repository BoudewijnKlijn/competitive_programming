import numpy as np

n = int(100E3)
m = 6
cats = np.zeros(n-1, dtype=int)
# some vertices contain a cat
idxs = np.random.randint(1, n, n//1000)
cats[idxs] = 1
edges = list(zip(range(1, n), range(2, n+1)))
# print(edges)
# print(len(edges))
#
# print(cats)
# print(cats.sum())
with open('in3', 'w') as fp:
    fp.write(f'{n} {m}\n')
    fp.write(f'{" ".join(map(str, cats))}')
    for edge in edges:
        fp.write(f'\n{edge[0]} {edge[1]}')
