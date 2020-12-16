import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib import transforms
from scipy.stats import multivariate_normal as mvnd
from math import sqrt


def rvs2d(size=10, rho=1):
    return tuple(zip(*mvnd.rvs((0, 0), [[1, rho], [rho, 1]], size=size)))


def mixed(size):
    r = mvnd.rvs((0, 0), [[1, 0.9], [0.9, 1]], size=int(size*0.9))
    np.append(r, mvnd.rvs((0, 0), [[1, -0.9], [-0.9, 1]], size=size-int(size*0.9)))
    return tuple(zip(*r)) 


def pearson(x, y):
    if len(x) != len(y):
        raise ValueError("Two selections have to have same size!")
    n = len(x)
    xm = sum(x) / n
    ym = sum(x) / n
    cov = sum([(x[i] - xm)*(y[i] - ym) for i in range(n)])
    ss = sqrt(sum([(x[i]-xm)**2 for i in range(n)]) * \
              sum([(y[i]-ym)**2 for i in range(n)]))
    return cov / ss


def quadrant(x, y):
    if len(x) != len(y):
        raise ValueError("Two selections have to have same size!")
    xm = np.median(x)
    ym = np.median(y)
    sign = lambda x: 1 if x > 0 else -1 if x < 0 else 0
    return sum(map(lambda a: sign((a[0]-xm)*(a[1]-ym)), zip(x, y))) / len(x)

def spearman(x, y):
    sx = sorted(x)
    sy = sorted(y)
    rx = [sx.index(a) for a in x]
    ry = [sy.index(a) for a in y]
    return pearson(rx, ry)

def plotEllipse(x, y, ax, sigmas):
    r = pearson(x, y)
    ellipse = Ellipse((0, 0),
                      width=sqrt(1 + r),
                      height=sqrt(1 - r),
                      facecolor='none',
                      edgecolor='red')
    xm = sum(x) / len(x)
    ym = sum(y) / len(y)
    sx = sqrt(sum(map(lambda a: (a - xm)**2, x)) / len(x))
    sy = sqrt(sum(map(lambda a: (a - ym)**2, y)) / len(y))
    tr = transforms.Affine2D() \
         .rotate_deg(45) \
         .scale(sx * sigmas, sy * sigmas) \
         .translate(xm, ym)
    ellipse.set_transform(tr + ax.transData)
    ax.add_patch(ellipse)
    ax.scatter(x, y, s=0.9)
    
        
if __name__ == "__main__":
    s = rvs2d(size=100, rho=0.5)
    print(s)
    print(quadrant(*s))
    print(pearson(*s))
    print(spearman(*s))
    print(mixed(10))
    fig, ax = plt.subplots()
    plotEllipse(*s, ax, 3)
    plt.show()
