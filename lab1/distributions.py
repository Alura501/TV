from random import randrange
import math
import numpy as np
from typing import Tuple


MU = 0
SIGMA = 1
LAMBDA = 1
A = 0
B = 1


def get_distributions():
    ds = [Normal("Нормальное распределение", [0,1]),#mu=0, sigma=1
      Cauchy("Распределение Коши", [0,1]), #mu=0, lambda=1
      Laplace("Распределение Лапласа", [ 0, 2**(-0.5)]),#mu=0, lambda=2^(-0.5)
      Poisson("Распределение Пуассона", [ 10]),#mu=10
      Uniform("Равномерное распределение", [-3**0.5, 3**0.5])]#A=-3^(1/2), B=3^(1/2)
    return ds


def selection(dist, n: int):
    return sorted([dist.x() for i in range(n)])


def rand()->float:
    return randrange(1, 1000) / 1000



class Distribution:
    name: str
    parameters =[]

    def __init__(self, name: str, parameters):
        self.name = name
        self.parameters = parameters

    def x(self)->float:
        return 0
    
    def f(self, x: float)->float:
        return 0

    def F(self, x: float)->float:
        return 0

    def interval(self)->Tuple[float, float]:
        return (0, 0)

    def discrete(self):
        return False

class Normal(Distribution):
    laplas_table = np.zeros(1)
    
    def f(self, x:float)->float:
        s = self.parameters[SIGMA]
        m = self.parameters[MU]
        return math.exp(-(x - m)**2/(2*s))/(s*math.sqrt(2*math.pi))

    def x(self)->float:
        y = -6
        for i in range(12):
            y += rand()
        return self.parameters[MU] + self.parameters[SIGMA] * y

    def F(self, x:float)->float:
        if self.laplas_table.shape == (1,):
            self.laplas_table = np.zeros(400)
            f = open('laplas.txt')
            i = 0
            for line in f:
                self.laplas_table[i] = float(line.split()[1])
                i += 1
        y = (x - self.parameters[MU]) / self.parameters[SIGMA]
        n = math.floor(abs(y * 100))
        val = 0
        if n > 399:
            val = 0.9999
        else:
            val = self.laplas_table[n]
        if y > 0:
            return 0.5 + val / 2
        else:
            return 0.5 - val / 2

    def interval(self):
        s = self.parameters[SIGMA]
        m = self.parameters[MU]
        return (m - 4*s, m + 4*s)



class Cauchy(Distribution):
    def f(self, x: float)->float:
        l = self.parameters[LAMBDA]
        m = self.parameters[MU]
        return l / (math.pi * (l**2 + (x - m)**2))

    def F(self, x:float)->float:
        l = self.parameters[LAMBDA]
        m = self.parameters[MU]
        return 0.5 + math.atan((x - m)/l)/math.pi

    def x(self)->float:
        e = 0.0001
        l = self.parameters[LAMBDA]
        m = self.parameters[MU]
        while True:
            y = rand()
            if abs(y - 0.25) > e and abs(y - 0.75) > e:
                return m + l * math.tan(2*math.pi*y)

    def interval(self)->float:
        l = self.parameters[LAMBDA]
        m = self.parameters[MU]
        rng = math.sqrt(l * (300 - l))
        return (m - rng, m + rng)



class Laplace(Distribution):
    def f(self, x:float)->float:
        l = self.parameters[LAMBDA]
        m = self.parameters[MU]
        return 0.5 * l * math.exp(-l * abs(x - m))

    def F(self, x:float)->float:
        l = self.parameters[LAMBDA]
        m = self.parameters[MU]
        if x < m:
            return 0.5 * math.exp(l * (x - m))
        else:
            return 1 - 0.5 * math.exp(-l * (x - m))

    def x(self):
        l = self.parameters[LAMBDA]
        m = self.parameters[MU]
        return m + math.log(rand() / rand()) / l

    def interval(self):
        l = self.parameters[LAMBDA]
        m = self.parameters[MU]
        rng = -math.log(0.002 / l)/l
        return (m - rng, m + rng)


class Poisson(Distribution):
    def f(self, x: float)->float:
        if x < 0:
            return 0
        m = self.parameters[MU]
        n = math.floor(x)
        v = math.exp(-m)
        for i in range(1, n+1):
            v *= m / i
        return v

    def F(self, x:float)->float:
        if x < 0:
            return 0
        m = self.parameters[MU]
        k = math.ceil(x)
        v = math.exp(-m)
        s = v
        for i in range(1, k):
            v *= m / i
            s += v
        return s

    def x(self)->float:
        m = self.parameters[MU]        
        p = math.exp(-m)
        r1 = rand() - p
        x = 0
        while r1 > 0:
            x += 1
            p *= m / x
            r1 -= p
        return x

    def interval(self):
        return (0, self.parameters[MU]*3)

    def discrete(self):
        return True


class Uniform(Distribution):
    def f(self, x:float)->float:
        a = self.parameters[A]
        b = self.parameters[B]
        if x < a or x > b:
            return 0
        else:
            return 1 / (b - a)

    def F(self, x:float)->float:
        a = self.parameters[A]
        b = self.parameters[B]
        if x < a:
            return 0
        elif x > b:
            return 1
        else:
            return (x - a) / (b - a)

    def x(self)->float:
        a = self.parameters[A]
        b = self.parameters[B]        
        return a + (b - a)*rand()

    def interval(self):
        a = self.parameters[A]
        b = self.parameters[B]
        return (a, b)


