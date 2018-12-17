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

    def b_spline_value(self, i, k, x):
        """Calculate b-spline b_spline_valueue in point t

        t -- normalized point
        """
        if (x < self.points[i] or x > self.points[i + k + 1]):
            return 0
        if (k == 0):
            if (x >= self.points[i] and x < self.points[i + 1]):
                return 1
            return 0
        else:
            if (self.points[i] != self.points[i + k]):
                a = (x - self.points[i]) / (self.points[i + k] - self.points[i])
            else:
                a = 0
            if (self.points[i + 1] != self.points[i + k + 1]):
                b = (self.points[i + k + 1] - x) / (self.points[i + k + 1] - self.points[i + 1])
            else:
                b = 0
            return a * self.b_spline_value(i, k - 1, x) + b * self.b_spline_value(i + 1, k - 1, x)

    def fit(self, knots, values):
        self.m = len(values)
        self.n = len(self.points) - self.deg - 1
        A = np.zeros((self.n, self.n))
        # form A
        for i in range(self.n):
            for j in range(self.n):
                if abs(i - j) <= self.deg:
                    A[i, j] = sum([self.b_spline_value(i, self.deg, x) * self.b_spline_value(j, self.deg, x) for x in knots])
        # form b
        b = np.zeros((self.n, ))
        for j in range(self.n):
            b[j] = sum([values[i] * self.b_spline_value(j, self.deg, knots[i]) for i in range(self.m)])
        # print(A)
        # print(b)
        self.alpha = np.linalg.solve(A, b)
        return self

    def value(self, x):
        if (x < self.points[0] or x > self.points[-1]):
            return 0
        return sum([self.alpha[i] * self.b_spline_value(i, self.deg, x) for i in range(self.n)])

    def basis(self):
        knots = np.linspace(self.points[0], self.points[-1], 10 * (len(self.points) - self.deg))
        val = []
        for i in range(len(self.points) - self.deg - 1):
            val.append([self.b_spline_value(i, 2, knot) for knot in knots])
        return knots, val


def get_x(length):
    x = np.zeros(length)
    for i in range(length):
        x[i] = i + 1.0 / (i + 1) * np.random.rand()
    x = np.concatenate((x, x), 0)
    x = np.sort(x)

    return x


def get_data_1():
    x = get_x(60)
    n = len(x)
    y = [0] * n
    w = [1] * n
    for i in range(0, n, 2):
        y[i] = np.cos(0.2 * x[i])
        err = np.random.rand() * 15 / (x[i] + 10)
        y[i + 1] = y[i] + err
        y[i] -= err
        w[i] = 1.0 / math.fabs(x[i] - x[i - 1])
        w[i + 1] = w[i]

    return x, y

def get_data_2():
    x = get_x(10)
    n = len(x)
    y = [0] * n
    w = [1] * n
    for i in range(0, n, 2):
        y[i] = np.cos(0.2 * x[i])
        y[i] += 0.4 * np.cos(0.5 * x[i])
        err = np.random.rand() / 3
        y[i + 1] = y[i] + err
        y[i] -= err
        w[i] = 1.0 / math.fabs(x[i] - x[i - 1])
        w[i + 1] = w[i]

    return x, np.array(y)

if __name__  == '__main__':
    np.set_printoptions(precision=3, suppress=True)
    # x, y = get_data_1()
    x, y = get_data_2()
    points = np.linspace(x[0], x[6], 6)
    points = np.append(points, (x[-1], ))

    # spline = CubicBSpline(points)
    # knots, values = spline.basis()
    # for list in values:
    #     plt.plot(knots, list)

    spline = CubicBSpline(points).fit(x, y)
    v = np.linspace(x[0], x[-1] - 0.05, 1000)
    f = [spline.value(e) for e in v]
    v2 = points
    f2 = [spline.value(p) for p in v2]
    plt.plot(x, y, 'o', v, f, v2, f2, 's')
    plt.xlim(points[0] - 1, points[-1] + 1)
    plt.legend(['Данные', 'Сплайн', 'Узлы сплайна'])
    plt.show()
