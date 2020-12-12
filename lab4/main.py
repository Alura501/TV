from math import sqrt, exp, floor, pi
import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append('../lab1')
import distributions as dst


def kernel_function(x: float):
    return exp(-x*x/2)/sqrt(2*pi)


def kernel_approximation(xs: np.ndarray, sel: np.ndarray, k):
    n = len(sel)
    s = sqrt((sel*sel).sum()/n - (sel.sum()/n)**2)
    h = 1.06*s*(n**(-0.2))*k
    res = np.zeros_like(xs)
    for i in range(len(xs)):
        for v in sel:
            res[i] += kernel_function((xs[i] - v)/h)
        res[i] /= n*h
    return res


ds = dst.get_distributions()
ns = [20, 60, 100]
ks = [0.5, 1, 2]

for d in ds:
    fig, ax = plt.subplots(len(ks), len(ns))
    rng = (-4, 4) if not d.discrete() else (6, 14)
    for i in range(len(ns)):
        sel = np.array(dst.selection(d, ns[i]))
        x = np.linspace(*rng, 100)
        y1 = list(map(d.f, x))
        for j in range(len(ks)):
            y2 = kernel_approximation(x, sel, ks[j])
            ax1 = ax[i, j]
            ax1.plot(x, y1, label='теор')
            ax1.plot(x, y2, label='оценка')
            ax1.legend()
            ax1.set_xlabel('x' if i == len(ns) - 1 else '')
            ax1.set_ylabel(f'$f(x), n = {ns[i]}$')
            if i == 0:
                ax1.set_title((d.name if j == 1 else '') + f"\n\n$h = h_n * {ks[j]}$")
    plt.show()


for d in ds:
    fig, ax = plt.subplots(1, len(ns))
    rng = (-4, 4) if not d.discrete() else (6, 14)
    for i in range(len(ns)):
        data = [d.x() for j in range(ns[i])]
        x = np.linspace(min(data), max(data), 200)
        yF = [d.F(k) for k in x]
        plt.subplot(1, 3, i+1)
        plt.title(d.name + ", n = " + str(ns[i]))
        plt.xlabel('x')
        plt.ylabel('Функция распределения')
        plt.plot(x, yF, label='ожидаемое')
        plt.hist(data, density=True, label='полученное', bins=floor(len(data)),histtype='step',cumulative=True)
        plt.legend()
    plt.show()
