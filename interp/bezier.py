#!/usr/bin/python3
#-*- coding: UTF-8 -*-

import numpy as np
from numpy import pi
import TDMAsolver


class Bezier:
    def __init__(self):
        pass

    def fit(self, knots, values, d0, dn):
        """Fit spline to given values known in knots.

        Keyword arguments:
        knots -- knots
        values -- given values
        d0 -- derivative in knots[0]
        dn -- derivative in knots[n]
        """
        self.knots = knots
        self.h = knots[1] - knots[0]
        self.n = len(knots)

        # form the tridiagonal matrix to compute derivatives d[1], ..., d[n-1]
        # below diagonal 
        a = [1.0] * (self.n - 1)
        a[-1] = 0.0
        # main diagonal
        b = [4.0] * self.n
        b[0] = b[-1] = 1.0
        # above diagonal
        c = [1.0] * (self.n - 1)
        c[0] = 0.0

        # form the known-values vector Y
        Y = np.zeros((self.n))
        Y[0] = d0
        Y[1 : self.n - 1] = [3.0 * (values[i + 2] - values[i]) for i in range(self.n - 2)]
        Y[self.n - 1] = dn

        # compute the derivatives vector D with Tridiagonal Matrix Algorithm
        D = TDMAsolver.TDMAsolver(a, b, c, Y)

        # Control Points
        self.T = np.zeros((self.n, 4))
        for i in range(self.n - 1):
            self.T[i][0] = values[i]
            self.T[i][1] = D[i] + 3 * values[i]
            self.T[i][2] = 3 * values[i + 1] - D[i + 1]
            self.T[i][3] = values[i + 1]
        return self

    def value(self, x):
        """Compute value in given knot.

        Keyword arguments:
        knot -- given knot, must be in interval [x[0], ..., x[n]]
        """
        if (x < self.knots[0]) or (x > self.knots[self.n - 1]):
            return None
        i = [j for j in range(len(self.knots)-1) if (x >= self.knots[j] and x <= self.knots[j + 1])][0]
        t = (x - self.knots[i]) / self.h
        t_i = np.array([
            (1 - t) ** 3,
            ((1 - t) ** 2) * t,
            (1 - t) * (t ** 2),
            t ** 3
        ])
        return t_i.dot(self.T[i])

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    knots = np.arange(0.0, 8 * pi + 0.1, pi / 4)
    values = knots * np.sin(knots) + np.log(knots + 1)
    d = np.divide(1, (knots + 1)) + np.sin(knots) + knots * np.cos(knots)
    x = np.arange(0.0, 8 * pi, 0.05)
    Bzr = Bezier().fit(knots, values, d[0], d[-1])
    f = [Bzr.value(e) for e in x]
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