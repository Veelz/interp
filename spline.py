import numpy as np
from numpy import pi
import matplotlib.pyplot as plt


class Spline:
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
        self.knots = np.array(knots)
        self.n = len(knots)
        self.values = np.array(values)
        h = knots[1] - knots[0]

        # form the matrix T to compute derivatives d[1], ..., d[n-1]
        vec = [1.0, 4.0, 1.0]
        T = np.zeros((self.n, self.n))
        T[0, 0] = T[self.n - 1, self.n - 1] = 1.0
        for i in range(1, self.n - 1):
            T[i][i - 1 : i + 2] = vec

        # form the known-values vector Y
        Y = np.zeros((self.n))
        Y[0] = d0
        Y[1 : self.n - 1] = [3.0 / h * (self.values[i + 2] - self.values[i]) for i in range(self.n - 2)]
        Y[self.n - 1] = dn

        # solve the linear system to find the derivatives vector D 
        D = np.linalg.solve(T, Y)
        # compute the coefficients in matrix form
        s = np.array([
            [1.0, 0, 0, 0],
            [0, 1.0, 0, 0],
            [-3.0 / (h ** 2), -2.0 / h, 3.0 / (h ** 2), -1.0 / h],
            [2.0 / (h ** 3), 1.0 / (h ** 2), -2.0 / (h ** 3), 1.0 / (h ** 2)]
        ])
        p = np.transpose([[self.values[i], D[i], self.values[i + 1], D[i + 1]] for i in range(self.n - 1)])
        self.A = np.transpose(s.dot(p))
        return self

    def value(self, knot):
        """Compute value in given knot.

        Keyword arguments:
        knot -- given knot, must be in interval [x[0], ..., x[n]]
        """
        if self.A is None:
            return None
        if (knot < self.knots[0]) or (knot > self.knots[self.n - 1]):
            return None

        i = [j for j in range(len(self.knots)-1) if (knot >= self.knots[j] and knot <= self.knots[j + 1])][0]
        x_i = np.array([
            1,
            (knot - self.knots[i]),
            (knot - self.knots[i]) ** 2,
            (knot - self.knots[i]) ** 3,
        ])
        return x_i.dot(self.A[i])
    
    def valuesx(self, x):
        """Compute values in given knots.

        Keyword arguments:
        knots -- given knots, must be in interval [x[0], ..., x[n]]
        """
        if self.A is None:
            return None
        return [self.value(value) for value in x]


if __name__ == "__main__":
    knots = np.arange(0.0, 8 * pi + 0.1, pi / 4)
    values = knots * np.sin(knots) + np.log(knots + 1)
    d = np.divide(1, (knots + 1)) + np.sin(knots) + knots * np.cos(knots)
    x = np.arange(0.0, 8 * pi, 0.05)
    f = Spline().fit(knots, values, d[0], d[-1]).valuesx(x)
    true_values = x * np.sin(x) + np.log(x + 1)
    SSE = np.sum([(f[i] - true_values[i]) ** 2 for i in range(len(x))])

    line1, = plt.plot(knots, values, 'ro', label="Заданные значения")
    line2, = plt.plot(x, f, label="Интерполяция")
    legend1 = plt.legend(handles=[line1], loc=1)
    ax = plt.gca().add_artist(legend1)
    plt.legend(handles=[line2], loc=4)
    
    plt.grid(True)
    plt.xlabel("Сумма квадратов отклонений SSE=%.5f" % SSE)
    plt.show()
