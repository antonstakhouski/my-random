#!/usr/bin/env python

import sys
import math
import matplotlib.pyplot as plt

ARR_LEN = 1000000


class Random:
    def __init__(self, r0, a, m):
        self.r0 = r0
        self.a = a
        self.m = m

    def seed(self, value):
        self.r0 = value

    def rand(self):
        self.seed((self.a * self.r0) % self.m)
        return self.r0 / self.m


def print_hist(lst):
    #  plt.hist(lst, bins=20)
    plt.hist(lst, bins=20)
    #  plt.plot(lst, 'r--', linewidth=1)
    plt.grid(True)
    plt.show()


def calc_params(lst):
    mx = (1 / len(lst)) * sum(lst)
    sumsqr = 0
    for xi in lst:
        sumsqr += (xi - mx) ** 2
    dx = (1 / (len(lst) - 1)) * sumsqr
    sigma = math.sqrt(dx)
    print("~Mx = %f" % mx)
    print("~Dx = %f" % dx)
    print("~Sigma = %f" % sigma)
    return (mx, dx, sigma)


def uniformity_test(lst):
    k = 0
    for i in range(0, len(lst) // 2):
        if (lst[2 * i] ** 2) + (lst[(2 * i) + 1] ** 2) < 1:
            k += 1
    print("%f -> %f" % ((2 * k / len(lst)), (math.pi / 4)))


def aperiodic_test(a, r0, m):
    random = Random(r0, a, m)
    lst1 = list()
    for i in range(0, ARR_LEN):
        lst1.append(random.rand())
    xv = lst1[-1]

    random.seed(r0)
    lst2 = list()
    for i in range(0, ARR_LEN):
        lst2.append(random.rand())
    i1 = -1
    i2 = -1
    for i in range(0, ARR_LEN):
        if (lst1[i] == xv) and (lst2[i] == xv) and (i1 == -1):
            i1 = i
            continue
        if (lst1[i] == xv) and (lst2[i] == xv) and (i2 == -1):
            i2 = i
            break
    p = i2 - i1
    xp = lst2[p]

    lst1 = list()
    for i in range(0, ARR_LEN):
        lst1.append(random.rand())
    random.seed(xp)
    lst2 = list()
    for i in range(0, ARR_LEN):
        lst2.append(random.rand())
    i3 = -1
    for i in range(0, ARR_LEN - p):
        if (lst1[i] == lst1[i + p]) and (lst2[i] == lst2[i + p]):
            i3 = i
            break
    l = i3 + p
    print("P = %d" % p)
    print("L = %d" % l)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Using: " + sys.argv[0] + " a R0 m")
        exit(0)
    a = int(sys.argv[1])
    r0 = int(sys.argv[2])
    m = int(sys.argv[3])

    random = Random(r0, a, m)
    lst = list()
    for i in range(0, ARR_LEN):
        lst.append(random.rand())

    calc_params(lst)
    uniformity_test(lst)
    aperiodic_test(a, r0, m)
    print_hist(lst)
