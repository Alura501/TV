import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal as mvnd
from functions import *

def count_coefs(gen_sel, N):
    rs = [[0, 0], [0, 0], [0, 0]]
    f = [pearson, spearman, quadrant]
    for i in range(N):
        s = gen_sel()
        for k in range(len(rs)):
            r = f[k](*s)
            rs[k][0] += r / N
            rs[k][1] += r**2 / N
    print('\tr\t\t\trs\t\t\trq')
    s1, s2, s3, s4 = 'E', 'E2', 'D', 's'
    for i in range(len(rs)):
        s1 += f'\t{rs[i][0]}'
        s2 += f'\t{rs[i][1]}'
        s3 += f'\t{rs[i][1] - rs[i][0]**2}'
        s4 += f'\t{np.sqrt(rs[i][1] - rs[i][0]**2)}'
    print('\n'.join([s1, s2, s3, s4]))

rs = [0, 0.5, 0.9]
ns = [20, 60, 100]
N = 1000


for i in range(len(ns)):
    fig, ax = plt.subplots(1, 3)
    print(f'\n\n\t\tn = {ns[i]}\n')
    for j in range(len(rs)):
        a = ax[j]
        s = rvs2d(ns[i], rs[j])
        a.set_title(f'n = {ns[i]},'+r' $\rho '+f'= {rs[j]}$')
        a.axis('equal')
        plotEllipse(*s, a, 3)
        print(f'\nr = {rs[j]}\n')
        count_coefs(lambda: rvs2d(ns[i], rs[j]), N)
    print(f'\nmixed\n')
    count_coefs(lambda: mixed(ns[i]), N)
    plt.show()
