import matplotlib.pyplot as plt
import numpy as np
from histogram import Histogram
import distributions as dst

k=1

for d in dst.get_distributions():
    for n in [10, 100, 1000]:
        data = [d.x() for i in range(n)]
        hs = Histogram(data, d.discrete())
        x = np.linspace(min(data), max(data), 200)
        yf = [d.f(k) for k in x]
        yF = [d.F(k) for k in x]
        plt.subplot(2, 3, k)
        plt.title(d.name + ", n = " + str(n))
        plt.xlabel('x')
        plt.ylabel('Функция плотности')
        plt.plot(x, yf, label='ожидаемое')
        widthBars= np.empty(len(hs.x))
        for i in range(len(hs.x)-1):
            widthBars[i]=hs.x[i+1]-hs.x[i]
        widthBars[len(hs.x)-1]=hs.x[len(hs.x)-1]-hs.x[len(hs.x)-2]
        b1= plt.bar(hs.x, hs.y, label='полученное', color='orange', edgecolor='black', linewidth=0.5, width=widthBars)
        plt.legend()
        plt.subplot(2, 3, k+3)
        plt.xlabel('x')
        plt.ylabel('Функция распределения')
        plt.plot(x, yF, label='ожидаемое')
        b2= plt.bar(hs.x, hs.F(), label='полученное', color='orange', edgecolor='black', linewidth=0.5, width=widthBars)
        plt.legend()
        k=k+1
    k=1
    plt.show()
