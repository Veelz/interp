import math
import numpy as np
import matplotlib.pyplot as plt

class CubicBSpline:
    def __init__(self, points):
        # degree
        self.deg = 3
        self.points = np.concatenate((np.full((self.deg,), points[0]), 
            np.array(points), 
            np.full((self.deg,), points[-1])))
        self.n = len(self.points) - self.deg - 1

    def b_spline_value(self, id, x):
        """Calculate b-spline valueue in point x

        x -- normalized point
        """
        if (x < self.points[id] or x > self.points[id + self.deg + 1]):
            return 0
    
        buff = [0] * (self.deg + 1)
        l = id
        while (l < self.n and (self.points[l] > x or self.points[l + 1] <= x)):
            l += 1
    
        buff[id - l + self.deg] = 1
        for j in range(1, self.deg + 1):
            for i in reversed(range(l - self.deg + j, l + 1)):
                if self.points[i + 1 + self.deg - j] == self.points[i]:
                    alpha = 0
                else:
                    alpha = (x - self.points[i]) / (self.points[i + 1 + self.deg - j] - self.points[i])
                buff[i - l + self.deg] = alpha * buff[i - l + self.deg] + (1 - alpha) * buff[i - 1 - l + self.deg]
        return buff[self.deg]

    def fit(self, knots, values):
        self.m = len(values)
        # self.n defined
        A = np.zeros((self.n, self.n))
        # form A
        for i in range(self.n):
            for j in range(self.n):
                if abs(i - j) <= self.deg:
                    A[i, j] = sum([self.b_spline_value(i, x) * self.b_spline_value(j, x) for x in knots])
        # form b
        b = np.zeros((self.n, ))
        for j in range(self.n):
            b[j] = sum([values[i] * self.b_spline_value(j, knots[i]) for i in range(self.m)])
        print(A)
        print(b)
        self.alpha = np.linalg.solve(A, b)
        return self

    def value(self, x):
        if (x < self.points[0] or x > self.points[-1]):
            return 0
        return sum([self.alpha[i] * self.b_spline_value(i, x) for i in range(self.n)])

    def basis(self):
        knots = np.linspace(self.points[0], self.points[-1], 10 * (len(self.points) - self.deg))
        val = []
        for i in range(len(self.points) - self.deg - 1):
            val.append([self.b_spline_value(i, knot) for knot in knots])
        return knots, val
