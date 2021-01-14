import numpy as np
from scipy.stats import laplace, norm, uniform


def norm_mle_cdf(selection):
    x = np.array(selection)
    xm = np.mean(selection)
    s = np.sqrt(np.mean(x*x) - xm**2)
    return lambda x: norm.cdf(x, xm, s)


def count(x, xmin, xmax):
    c = 0
    for v in x:
        c += 1 if xmin <= v < xmax else 0
    return c


def tr(s, n):
    if isinstance(s, str):
        try:
            i = s.index('.')
        except ValueError:
            return s
        return s[:min(i + n + 1, len(s))]
    return tr(str(s), n)

def table(sel, k, file):
    file.write(r'\begin{tabular}{|c|c|c|c|c|c|c|}' + '\n')
    file.write(r'\hline $i$ & $\Delta_i$ & $n_i$ & $p_i$ & $np_i$ & $\frac{(n_i-np_i)^2}{np_i}$\\' + '\n')
    x = np.array(sel)
    x.sort()
    d = (x[-1] - x[0]) / k
    F = norm_mle_cdf(x)
    n = len(x)
    chi = 0
    for i in range(k):
        if i == 0:
            a0 = r'-\infty'
            a1 = round(x[0] + d, 2)
            p = round(F(a1), 4)
            ni = count(x, x[0] - 1, a1)
        elif i == k - 1:
            a0 = round(x[0] + d*i, 2)
            a1 = r'+\infty'
            p = round(1 - F(a0), 4)
            ni = count(x, a0, x[-1] + 1)
        else:
            a0 = round(x[0] + d*i, 2)
            a1 = round(a0 + d, 2)
            p = round(F(a1) - F(a0), 4)
            ni = count(x, a0, a1)
        s = f'\\hline {i + 1} & $({tr(a0, 2)}; {tr(a1, 2)})$ & {ni} & {tr(p, 4)} & '
        s += f' {tr(ni-n*p, 2)} & '
        dchi = round((ni-n*p)**2 / (n*p), 2)
        s += f'{tr(dchi, 4)} ' + r'\\'
        chi += dchi
        file.write(s + '\n')
    chi = round(chi, 2)
    file.write(f'\\hline $\Sigma$ & - & {n} & 1.0000 & {n}.00 & 0.00 & ' + tr(chi, 2) + ' \\\\\n')
    file.write('\\hline\n\\end{tabular}\n')
    file.write(r'\providecommand{\mychi}{}\renewcommand{\mychi}{' + tr(chi, 2) + '}\n')
    return chi

class UniformWrapper:
    @staticmethod
    def rvs(size=10):
        return uniform.rvs(size=size, loc=-np.sqrt(3), scale=2*np.sqrt(3))
    
N = [100, 20, 20]
K = [8, 5, 5]
chi = [14.0671, 9.4877, 9.4877]
dirname = r'C:\\Users\\Луиза\\Desktop\\5 sem\\теорвер\\практика\\отчеты\\лаб7'
dst = [norm, laplace, UniformWrapper]

for i in range(3):
    sel = dst[i].rvs(size=N[i])
    print(f'mu = {np.mean(sel)}, s = {np.sqrt(np.mean(sel*sel) - np.mean(sel)**2)}')
    with open(dirname + '\\' + f'tb{i+1}.tex', 'w') as f:
        c = table(sel, K[i], f)
        f.write(r'\providecommand{\tbchi}{}\renewcommand{\tbchi}{' + tr(chi[i], 3) + '}\n')
        print(f'chi: {chi[i]}; my chi: {c}')


