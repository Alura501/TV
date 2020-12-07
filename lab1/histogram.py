from math import ceil, sqrt, floor
import numpy as np


# класс преобразует входные данные
# в два массива: [x1 .. xn] и [f^(x1) .. f^(xn)]
class Histogram:
    def __init__(self, data, discrete=False):
        n = len(data)
        min_x = min(data)
        max_x = max(data)
        b = self.bins(n)
        if discrete:
            b = max_x - min_x
        self.h = (max_x - min_x) / b
        self.x = np.array([min_x + (i + 1)*self.h for i in range(b)])
        self.y = np.zeros(b)
        for val in data:
            if val == max_x:
                self.y[-1] += 1 / (n * self.h)
                continue
            i = floor((val - min_x) / self.h)
            self.y[i] += 1 / (n * self.h)

    def F(self):
        return np.cumsum(self.y * self.h)
      
    @staticmethod
    def bins(n: int):
        return ceil(sqrt(n))

   
