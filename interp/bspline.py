#!/usr/bin/python3
#-*- coding: UTF-8 -*-

import math
import numpy as np
from numpy import pi


class CubicBSpline:
    def __init__(self):
        self.T = 1 / 6 * np.transpose([
            [0, 4, -44, 64],
            [0, -12, 60, -48],
            [0, 12, -24, 12],
            [1, -3, 3, -1]
        ])
        # normalized knots
        self.knots = np.linspace(0.0, 4.0, 5)

    def b_spline_value(self, t):
        """Calculate b-spline value in point t

        t -- normalized point
        """
        if (t < self.knots[0]) or (t >= self.knots[-1]):
            return 0.0
        else:
            i = [j for j in range(len(self.knots)-1) if (t >= self.knots[j] and t < self.knots[j + 1])][0]
            vec = [1.0, t, t * t, t * t * t]
            return self.T[i].dot(vec)

    def __base_func0(self, points):
        return [self.b_spline_value(x) for x in points]

    def __base_func(self, i, points):
        if i == 0:
            return self.__base_func0(points)
        else:
            return self.__base_func0(np.array(points) - i)

    def fit(self, knots, values, d0, dn):
        """Fit spline to given values known in knots.

        Keyword arguments:
        knots -- knots
        values -- given values
        d0 -- derivative in knots[0]
        dn -- derivative in knots[n]
        """
        self.knots_x = knots
        self.h = self.knots_x[1] - self.knots_x[0]
        # expand knots with additional knots.
        n = len(knots) + 2
        # coefficients vector in knots
        b = self.__base_func(0, np.arange(3.0, 0.0, -1.0))
        # form the matrix T to compute alphas
        T = np.zeros((n, n))
        T[0, 0] = T[-1, -3] = -0.5
        T[0, 2] = T[-1, -1] = 0.5
        for i in range(1, n - 1):
            T[i][i - 1 : i + 2] = b
        # known-value vector
        Y = np.zeros((n))
        Y[0] = d0
        Y[1 : n - 1] = values[0 : n - 2]
        Y[n - 1] = dn
        # compute the coefficients vector
        self.A = np.linalg.solve(T, Y)
        return self

    def value(self, x):
        """Compute value in given knot.

        Keyword arguments:
        knot -- given knot, must be in interval [x[0], ..., x[n]]
        """
        if (x < self.knots_x[0]) or (x > self.knots_x[-1]):
            return None
        t = (x - self.knots_x[0]) / self.h + 3
        start = math.floor(t) - 3
        end = math.ceil(t)
        result = 0.0
        for i in np.arange(start, end):
            value = self.b_spline_value(t - i)
            result += self.A[i] * value
        return result


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    knots = np.arange(0.0, 8 * pi + 0.1, pi / 4)
    values = knots * np.sin(knots) + np.log(knots + 1)
    d = np.divide(1, (knots + 1)) + np.sin(knots) + knots * np.cos(knots)
    x = np.arange(0.0, 8 * pi, 0.05)

    BSp = CubicBSpline().fit(knots, values, d[0], d[-1])
    f = [BSp.value(e) for e in x]
    true_values = x * np.sin(x) + np.log(x + 1)

    SSE = np.sum([(f[i] - true_values[i]) ** 2 for i in range(len(x))])

    line1, = plt.plot(knots, values, 'ro', label="Заданные значения")
    line2, = plt.plot(x, f, label="Интерполяция")
    legend1 = plt.legend(handles=[line1], loc=1)
    ax = plt.gca().add_artist(legend1)
    plt.legend(handles=[line2], loc=4)
    plt.xlabel("Сумма квадратов отклонений SSE=%.5f" % SSE)

    plt.grid(True)
    plt.show()
