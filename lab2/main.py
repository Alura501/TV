import sys
sys.path.append('../lab1')
import distributions as dst
from math import sqrt


def sort(dist, n: int):
    return sorted(dist.x() for i in range(n))

def avr(sel: list): #среднее
    return sum(sel) / len(sel)

def med(sel: list): #медиана
    l = len(sel) // 2
    if len(sel) % 2 == 0:
        return (sel[l-1] + sel[l]) / 2
    else:
        return sel[l]

def zr(sel: list): #полусумма экстремальных элементов 
    return (sel[0] + sel[-1]) / 2

def zq(sel: list): #полусумма квартилей
    n = len(sel)
    z = 0
    if n % 4 == 0:
        z += sel[n // 4 - 1]
    else:
        z += sel[n // 4]
    if 3*n % 4 == 0:
        z += sel[3*n // 4 - 1]
    else:
        z += sel[3*n // 4]
    return z / 2

def ztr(sel: list):  #усеченное среднее
    r = len(sel) // 4
    selr = sel[r:-r]
    return sum(selr) / len(selr)

N = 1000
ds = dst.get_distributions()
chars = ['avr', 'med', 'zr', 'zq', 'ztr']
for d in ds:
    print(d.name)
    for n in [10, 100, 1000]:
        print(f'n={n}')
        res = {}
        for i in range(5):
            res[i] = [0, 0]
        for i in range(N):
            s = sort(d, n)
            z = avr(s)
            res[0][0] += z/N
            res[0][1] += z*z/N
            z = med(s)
            res[1][0] += z/N
            res[1][1] += z*z/N
            z = zr(s)
            res[2][0] += z/N
            res[2][1] += z*z/N
            z = zq(s)
            res[3][0] += z/N
            res[3][1] += z*z/N
            z = ztr(s)
            res[4][0] += z/N
            res[4][1] += z*z/N  
        for i in range(5):
            res[i][1] = res[i][1] - res[i][0]**2
        for ch in chars:
            print(ch, res[chars.index(ch)], sqrt(res[chars.index(ch)][1]))
