  
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt
import sys
sys.path.append('../lab1')

import distributions as dst

ds = dst.get_distributions()
ns = [20, 100]
N = 1000


def moustaches(sel):
    n = len(sel)
    q1 = sel[n // 4 - 1] if n % 4 == 0 else sel[n // 4]
    q3 = sel[3*n // 4 - 1] if 3*n % 4 == 0 else sel[3*n // 4]
    return q1 - 1.5*(q3-q1), q3 + 1.5*(q3-q1)

for d in ds:
    plt.boxplot([dst.selection(d, n) for n in ns],
                vert=True,
                labels=list(map(lambda n: f'n = {n}', ns)))
    plt.ylabel('x')
    plt.xlabel('Размер выборки')
    plt.title(d.name)
    plt.grid(True)
    plt.show()
    print(d.name, '\n')
    sp = [[0, 0] for _ in ns]
    for _ in range(N):
        for i in range(len(ns)):
            s = np.array(dst.selection(d, ns[i]))
            x1, x2 = moustaches(s)
            x = 0
            for v in s:
                if v < x1 or v > x2:
                    x += 1
            x /= ns[i]
            sp[i][0] += x/N
            sp[i][1] += x*x/N
    for i in range(len(ns)):
        print(f'n = {ns[i]}')
        print(f'\tE = {sp[i][0]}\n\td = {sqrt(sp[i][1])}')
    print()

