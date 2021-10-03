import numpy as np

array = np.random.randint(1, int(1E4), int(1E5))
string = ' '.join(map(str, array))

with open('in3', 'w') as fp:
    fp.write(string)
